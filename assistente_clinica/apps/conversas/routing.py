from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Essa regex captura o ID da URL: ws://host/ws/chat/123/
    re_path(r'ws/chat/(?P<conversa_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]