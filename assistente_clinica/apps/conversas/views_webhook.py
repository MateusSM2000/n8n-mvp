from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.conf import settings

@csrf_exempt
def notify_message(request):
    # segurança
    if request.headers.get("X-API-TOKEN") != settings.NOTIFY_SECRET:
        return HttpResponse("Unauthorized", status=401)

    if request.method != "POST":
        return HttpResponse(status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except:
        return HttpResponse("Invalid JSON", status=400)

    conversa_id = data.get("conversa_id")
    mensagem = data.get("mensagem")
    tipo = data.get("tipo")

    if not conversa_id or not mensagem or not tipo:
        return HttpResponse("Missing fields", status=400)

    # Envia via websocket
    group_name = f"chat_{conversa_id}"
    async_to_sync(get_channel_layer().group_send)(
        group_name,
        {
            "type": "chat_message",
            "mensagem": mensagem,
            "tipo": tipo
        }
    )

    return HttpResponse("OK")