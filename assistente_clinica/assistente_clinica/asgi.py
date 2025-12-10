"""
ASGI config for assistente_clinica project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from apps.conversas import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assistente_clinica.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws/chat/<int:conversa_id>/", consumers.ChatConsumer.as_asgi()),
    ]),
})
