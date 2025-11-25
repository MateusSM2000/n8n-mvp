from django.contrib import admin
from .models import Produto, Categoria, PedidoPersonalizado

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "categoria", "preco", "ativo")
    list_filter = ("categoria", "ativo")
    search_fields = ("nome",)
    ordering = ("nome",)
    list_editable = ("ativo",)


@admin.register(PedidoPersonalizado)
class PedidoPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ("id", "telefone_cliente", "tipo_produto", "status")
    list_filter = ("status",)
    search_fields = ("telefone_cliente", "tipo_produto")