from django.contrib import admin
from .models import Produto, Categoria, PedidoPersonalizado
from django.utils.html import format_html

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
    readonly_fields = ("preview",)

    def preview(self, obj):
        # se não houver imagem, retorna texto simples (sem format_html)
        if not obj or not getattr(obj, "imagem", None):
            return "(sem imagem)"

        # usa format_html corretamente: string com placeholder + argumento
        return format_html(
            '<img src="{}" width="80" style="border-radius:8px;"/>',
            obj.imagem.url
        )

    preview.short_description = "Preview"


@admin.register(PedidoPersonalizado)
class PedidoPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ("id", "telefone_cliente", "tipo_produto", "status")
    list_filter = ("status",)
    search_fields = ("telefone_cliente", "tipo_produto")