from django.db import models
from django.utils import timezone

# Create your models here.

class Conversa(models.Model):
    """
    Representa um cliente (conversa) que interage via WhatsApp.
    """

    id = models.AutoField(primary_key=True)
    telefone = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=100, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    ultima_interacao = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "conversas"
        ordering = ["-ultima_interacao"]

    def __str__(self):
        return self.nome or self.telefone

    @property
    def last_message(self):
        """
        Retorna o conteúdo da última mensagem (cliente ou agente).
        """
        msg = self.mensagens.order_by("-criado_em").first()
        return msg.conteudo if msg else ""

    @property
    def unread_count(self):
        """
        Retorna quantas mensagens do cliente ainda não foram tratadas.
        (Opcional - só funciona se você adicionar uma coluna 'lido')
        """
        return 0  # implementar no futuro se quiser


class Mensagem(models.Model):
    """
    Representa cada mensagem enviada ou recebida.
    """

    TIPO_CHOICES = [
        ("cliente", "Cliente"),
        ("agente", "Agente"),
    ]

    id = models.AutoField(primary_key=True)

    conversas = models.ForeignKey(
        Conversa,
        related_name="mensagens",
        on_delete=models.CASCADE
    )

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "mensagens"
        ordering = ["criado_em"]

    def __str__(self):
        return f"[{self.tipo}] {self.conteudo[:30]}..."