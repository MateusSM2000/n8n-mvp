from rest_framework import serializers
from .models import Categoria, Produto, ProdutoImagem, PedidoPersonalizado


class ProdutoImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoImagem
        fields = ["id", "imagem"]


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class ProdutoSerializer(serializers.ModelSerializer):
    imagens = ProdutoImagemSerializer(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = [
            "id",
            "nome",
            "categoria",
            "descricao",
            "ativo",
            "imagens",
            "criado_em",
            "atualizado_em"
        ]


class PedidoPersonalizadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoPersonalizado
        fields = "__all__"