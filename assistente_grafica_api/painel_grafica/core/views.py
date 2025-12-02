from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Categoria, Produto, PedidoPersonalizado
from .serializers import CategoriaSerializer, ProdutoSerializer, PedidoPersonalizadoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nome"]


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.filter(ativo=True).prefetch_related("imagens")
    serializer_class = ProdutoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nome", "descricao"]

    # GET /produtos/por_categoria/<id>/
    @action(detail=False, methods=["get"], url_path="por_categoria/(?P<categoria_id>[^/.]+)")
    def por_categoria(self, request, categoria_id=None):
        produtos = Produto.objects.filter(categoria_id=categoria_id, ativo=True)
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)

    # GET /produtos/buscar/?q=caneca
    @action(detail=False, methods=["get"], url_path="buscar")
    def buscar(self, request):
        termo = request.query_params.get("q", "")
        produtos = Produto.objects.filter(nome__icontains=termo, ativo=True)
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)


class PedidoPersonalizadoViewSet(viewsets.ModelViewSet):
    queryset = PedidoPersonalizado.objects.all()
    serializer_class = PedidoPersonalizadoSerializer