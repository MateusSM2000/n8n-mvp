from rest_framework import serializers
from .models import Categoria, Produto, PedidoPersonalizado

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = "__all__"


class PedidoPersonalizadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoPersonalizado
        fields = "__all__"