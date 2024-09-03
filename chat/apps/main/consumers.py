import logging

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import JsonWebsocketConsumer

from chat.apps.main.models import Chat, Room
from chat.services.authentication import validate_jwt

log = logging.getLogger(__name__)


class ChatWebsocketConsumer(JsonWebsocketConsumer):
    def connect(self) -> None:
        """
        Handle websocket connection.
        """
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        token = self.scope['query_string'].decode().split('token=')[1]

        user = validate_jwt(token)
        if not user:
            self.close()
            log.warning(f"User tried to connect to room {self.room_id} with invalid token")
            return

        log.info(f"User {user.id} trying to connect to room {self.room_id}")

        if not Room.objects.filter(name=self.room_id).exists():
            self.close()
            log.warning(f"User {user.id} tried to connect to invalid room {self.room_id}")
            return

        self.scope['user'] = user

        async_to_sync(self.channel_layer.group_add)(
            self.room_id,
            self.channel_name
        )

        self.accept()
        log.info(f"User {user.id} connected to room {self.room_id}")

    def receive_json(self, data, **kwargs) -> None:
        """
        Handle receiving JSON data from websocket.
        """
        if self.scope['user'].is_authenticated:
            message = data['msg']
            room = Room.objects.get(name=self.room_id)
            user = self.scope['user']

            chat = Chat(room=room, user=user, message=message)
            chat.save()

            async_to_sync(self.channel_layer.group_send)(self.room_id, {
                'type': 'send.data',
                'msg': message,
                'msg_at': str(chat.created_at),
                'user': user.username
            })
        else:
            self.close()

    def send_data(self, data) -> None:
        """
        Send data to the websocket.
        """
        self.send_json({
            'type': 'websocket.send',
            **data,
        })

    def disconnect(self, close_code) -> None:
        """
        Handle websocket disconnection.
        """
        log.info(f"User {self.scope['user'].id} disconnected from room {self.room_id}")

        async_to_sync(self.channel_layer.group_discard)(
            self.room_id, self.channel_name
        )

        raise StopConsumer()
