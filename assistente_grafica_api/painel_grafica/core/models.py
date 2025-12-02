from django.db import models

# Create your models here.

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name="produtos")
    tema = models.CharField(max_length=120, null=True, blank=True)  # ex: “pets”, “Geek”, “empresa”
    tipo_personalizacao = models.CharField(max_length=120, null=True, blank=True)  # ex: “sublimação”
    tags = models.CharField(max_length=255, null=True, blank=True)  # armazenar palavras separadas por vírgula
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class ProdutoImagem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="imagens")
    imagem = models.ImageField(upload_to="produtos/")
    descricao = models.CharField(max_length=255, null=True, blank=True)  # ex: “vista lateral”, “detalhe”
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagem de {self.produto.nome}"


class PedidoPersonalizado(models.Model):
    id = models.AutoField(primary_key=True)
    telefone_cliente = models.CharField(max_length=20, blank=True, null=True)
    # Ligação opcional com um produto base do catálogo
    produto_base = models.ForeignKey(
        "Produto",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pedidos"
    )
    tipo_produto = models.CharField(max_length=255, blank=True, null=True)
    tema = models.TextField(blank=True, null=True)
    instrucoes = models.TextField(blank=True, null=True)

    # imagens enviadas pelo cliente
    imagens_cliente = models.JSONField(default=list, blank=True)

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