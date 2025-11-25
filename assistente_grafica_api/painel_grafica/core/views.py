from rest_framework import viewsets
from .models import Categoria, Produto, PedidoPersonalizado
from .serializers import CategoriaSerializer, ProdutoSerializer, PedidoPersonalizadoSerializer


# Create your views here.

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class PedidoPersonalizadoViewSet(viewsets.ModelViewSet):
    queryset = PedidoPersonalizado.objects.all()
    serializer_class = PedidoPersonalizadoSerializer