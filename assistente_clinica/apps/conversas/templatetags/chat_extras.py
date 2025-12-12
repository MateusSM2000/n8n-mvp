from django import template
from django.utils import timezone
import datetime

register = template.Library()


@register.filter
def data_inteligente(dado):
    """
    Converte datetime ou date para: 'Hoje', 'Ontem', 'segunda-feira', ou 'dd/mm/aaaa'.
    Funciona com objetos 'datetime' (com hora) e 'date' (sem hora, vindo do regroup).
    """
    if not dado:
        return ""

    # 1. Descobre se é DateTime (tem hora) ou Date (só dia)
    # O isinstance(dado, datetime.datetime) precisa vir antes, pois datetime herda de date
    if isinstance(dado, datetime.datetime):
        if timezone.is_aware(dado):
            data = timezone.localtime(dado).date()
        else:
            data = dado.date()
    elif isinstance(dado, datetime.date):
        # Se já for date (caso do regroup), usa direto
        data = dado
    else:
        # Se for string ou outro tipo, retorna como está pra não quebrar
        return str(dado)

    # 2. Prepara o "Hoje" para comparação
    now = timezone.now()
    if timezone.is_aware(now):
        agora = timezone.localtime(now).date()
    else:
        agora = now.date()

    # 3. Cálculo da diferença
    diferenca = (agora - data).days

    if diferenca == 0:
        return "Hoje"
    elif diferenca == 1:
        return "Ontem"
    elif diferenca < 7 and diferenca > 0:
        dias = {
            0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira",
            3: "quinta-feira", 4: "sexta-feira", 5: "sábado", 6: "domingo"
        }
        return dias[data.weekday()]
    else:
        return data.strftime("%d/%m/%Y")