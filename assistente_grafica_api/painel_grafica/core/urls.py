from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProdutoViewSet, PedidoPersonalizadoViewSet

router = DefaultRouter()
router.register("categorias", CategoriaViewSet)
router.register("produtos", ProdutoViewSet)
router.register("personalizados", PedidoPersonalizadoViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)