from django.urls import path
from chat.apps.main import consumers

websocket_urlpatterns = [
    path('ws/<str:room_id>/', consumers.ChatWebsocketConsumer.as_asgi()),
]
