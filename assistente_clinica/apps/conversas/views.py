from django.shortcuts import render
from apps.conversas.models import Conversa, Mensagem
import requests
from django.http import HttpResponse
from pathlib import Path
import environ
import os
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

WHATSAPP_API_URL = env("WHATSAPP_API_URL")
WHATSAPP_TOKEN = env("WHATSAPP_TOKEN")

def messages_home(request):
    return render(request, "messages/index.html")


def list_conversations(request):
    conversas = Conversa.objects.order_by('-ultima_interacao')
    return render(request, "messages/conversation_list.html", {
        "conversas": conversas
    })

def load_chat(request, conversa_id):
    conversa = Conversa.objects.get(id=conversa_id)
    mensagens = Mensagem.objects.filter(conversas_id=conversa_id).order_by("criado_em")
    return render(request, "messages/chat.html", {
        "conversa": conversa,
        "mensagens": mensagens
    })

def send_message(request):
    msg = request.POST.get("mensagem")
    conversa_id = request.POST.get("conversa_id")

    conversa = Conversa.objects.get(id=conversa_id)

    # 1. Salva no banco
    Mensagem.objects.create(
        conversas_id=conversa_id,
        tipo="agente",
        conteudo=msg
    )

    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        f"chat_{conversa_id}",
        {
            "type": "chat_message",
            "mensagem": msg,
            "tipo": "agente"
        }
    )

    # 2. Chama API do WhatsApp
    payload = {
        "messaging_product": "whatsapp",
        "to": conversa.telefone,
        "type": "text",
        "text": {"body": msg}
    }

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        requests.post(WHATSAPP_API_URL, json=payload, headers=headers, timeout=5)
    except Exception as e:
        print("Erro ao enviar WhatsApp:", e)

    # 3. Retorna apenas o HTML da bolha da mensagem
    return render(request, "messages/partials/message_agent.html", {
        "msg": msg
    })