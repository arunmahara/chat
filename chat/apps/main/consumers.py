import logging

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import JsonWebsocketConsumer
from django.db.models import Q

from chat.apps.main.models import Chat, Room
from chat.apps.main.util import get_or_none
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

        room = get_or_none(Room, name=self.room_id)
        if not room:
            self.close()
            log.warning(f"User {user.id} tried to connect to invalid room {self.room_id}")
            return

        self.scope['user'] = user
        self.room = room

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
        if not self.scope['user'].is_authenticated:
            self.close()
            return

        data_type = data.get('type')
        if data_type == 'chat':
            self.handle_message(data['msg'])
        elif data_type == 'search':
            self.handle_search(data['query'])
        else:
            log.warning(f"Unknown message type received: {data}")
            self.close()
            return

    def handle_message(self, message: str) -> None:
        """
        Handle incoming chat message.
        """
        user = self.scope['user']

        chat = Chat(room=self.room, user=user, message=message)
        chat.save()

        async_to_sync(self.channel_layer.group_send)(self.room_id, {
            'type': 'send.data',
            'msg': message,
            'msg_at': str(chat.created_at),
            'user': user.username
        })

    def handle_search(self, query: str) -> None:
        """
        Handle search query and send results back to the client.
        """
        if query:
            chats = Chat.objects.filter(
                Q(room=self.room) & (Q(message__icontains=query) | Q(user__username__icontains=query))
            ).order_by('created_at')
        else:
            chats = Chat.objects.filter(room=self.room).order_by('created_at')

        results = [
            {
                'user': chat.user.username,
                'message': chat.message,
                'msg_at': str(chat.created_at)
            }
            for chat in chats
        ]

        self.send_json({
            'type': 'search_results',
            'results': results
        })

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
        async_to_sync(self.channel_layer.group_discard)(
            self.room_id, self.channel_name
        )

        raise StopConsumer()
