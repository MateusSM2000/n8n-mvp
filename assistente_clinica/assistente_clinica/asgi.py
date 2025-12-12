"""
ASGI config for assistente_clinica project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application

# Configura o Django antes de importar coisas do Channels
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assistente_clinica.settings') # Verifique o nome do seu projeto aqui
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import apps.conversas.routing  # Importe o seu arquivo de rotas criado acima

application = ProtocolTypeRouter({
    # Requisições HTTP (padrão Django)
    "http": get_asgi_application(),

    # Requisições WebSocket (Channels)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.conversas.routing.websocket_urlpatterns
        )
    ),
})