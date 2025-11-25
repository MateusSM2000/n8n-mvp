from django.db import models

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name="produtos")
    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class PedidoPersonalizado(models.Model):
    telefone_cliente = models.CharField(max_length=20, blank=True, null=True)
    tipo_produto = models.CharField(max_length=255, blank=True, null=True)
    tema = models.TextField(blank=True, null=True)
    instrucoes = models.TextField(blank=True, null=True)

    # URLs de imagens geradas pela IA
    urls_imagens_sugeridas = models.JSONField(default=list, blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("aberto", "Aberto"),
            ("em_andamento", "Em andamento"),
            ("concluido", "Concluído"),
        ],
        default="aberto"
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id}"