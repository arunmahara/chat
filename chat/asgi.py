"""
ASGI config for chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.conf import settings
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import OriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter

from chat.apps.main import routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')


application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': OriginValidator(
            AuthMiddlewareStack(
                URLRouter(routing.websocket_urlpatterns)
            ),
            allowed_origins=settings.CORS_ALLOWED_ORIGINS,
        )
    }
)
