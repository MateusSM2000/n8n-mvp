from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProdutoViewSet, PedidoPersonalizadoViewSet

router = DefaultRouter()
router.register("categorias", CategoriaViewSet)
router.register("produtos", ProdutoViewSet)
router.register("personalizados", PedidoPersonalizadoViewSet)

urlpatterns = [
    path("", include(router.urls)),
]