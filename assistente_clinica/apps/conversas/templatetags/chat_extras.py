from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def data_inteligente(data_hora):
    """
    Converte datetime para: 'Hoje', 'Ontem', 'segunda-feira', ou 'dd/mm/aaaa'
    """
    if not data_hora:
        return ""

    # Garante que está no timezone correto
    agora = timezone.localtime(timezone.now()).date()
    data = timezone.localtime(data_hora).date()

    diferenca = (agora - data).days

    if diferenca == 0:
        return "Hoje"
    elif diferenca == 1:
        return "Ontem"
    elif diferenca < 7:
        # Dias da semana (0=Segunda, 6=Domingo)
        dias = {
            0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira",
            3: "quinta-feira", 4: "sexta-feira", 5: "sábado", 6: "domingo"
        }
        return dias[data.weekday()]
    else:
        return data.strftime("%d/%m/%Y")