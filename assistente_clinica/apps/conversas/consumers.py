import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.conversa_id = self.scope['url_route']['kwargs']['conversa_id']
        self.room_group_name = f"chat_{self.conversa_id}"

        # entrar no grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # sair do grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recebe mensagem do WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["mensagem"]
        tipo = data["tipo"]

        # envia ao grupo inteiro
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "mensagem": message,
                "tipo": tipo
            }
        )

    # Recebida mensagem do grupo
    async def chat_message(self, event):
        message = event["mensagem"]

        await self.send(text_data=json.dumps({
            "mensagem": message,
            "tipo": event.get("tipo")
        }))