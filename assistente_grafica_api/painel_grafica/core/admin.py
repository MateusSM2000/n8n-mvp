from django.contrib import admin
from .models import Categoria, Produto, ProdutoImagem, PedidoPersonalizado
from django.utils.html import format_html

# Register your models here.

# -----------------------------------
# CATEGORIA
# -----------------------------------
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "criado_em", "atualizado_em")
    search_fields = ("nome",)
    ordering = ("nome",)


# -----------------------------------
# PRODUTO + IMAGENS
# -----------------------------------
class ProdutoImagemInline(admin.TabularInline):
    model = ProdutoImagem
    extra = 1
    readonly_fields = ("preview",)

    class Media:
        js = ("core/admin_preview.js",)

    def preview(self, obj):
        if obj and obj.imagem:
            return format_html(
                '<img src="{}" width="80" style="border-radius:6px;">',
                obj.imagem.url
            )
        return "(sem imagem)"
    preview.short_description = "Preview"


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "categoria", "ativo",)
    list_filter = ("categoria", "ativo")
    search_fields = ("nome", "descricao")
    ordering = ("nome",)
    inlines = [ProdutoImagemInline]
    readonly_fields = ("preview",)

    class Media:
        js = ("core/admin_preview.js",)

    def preview(self, obj):
        imagens = obj.imagens.all()

        if not imagens:
            return "(sem imagens)"

        html = ""
        for img in imagens:
            if img.imagem:
                html += f'<img src="{img.imagem.url}" width="120" style="border-radius:6px; margin:5px;">'

        return format_html(html)

    preview.short_description = "Preview"


# -----------------------------------
# PEDIDO PERSONALIZADO
# -----------------------------------
@admin.register(PedidoPersonalizado)
class PedidoPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ("id", "telefone_cliente", "produto_base", "status", "criado_em")
    list_filter = ("status", "produto_base")
    search_fields = ("telefone_cliente", "tipo_produto", "tema", "instrucoes")
    ordering = ("-criado_em",)

    readonly_fields = (
        "criado_em",
        "atualizado_em",
        "preview_imagens_cliente",
        "preview_imagens_sugeridas",
    )

    fieldsets = (
        ("Informações do cliente", {
            "fields": ("telefone_cliente",)
        }),
        ("Relacionamento", {
            "fields": ("produto_base",)
        }),
        ("Detalhes do pedido", {
            "fields": ("tipo_produto", "tema", "instrucoes")
        }),
        ("Imagens do cliente", {
            "fields": ("imagens_cliente", "preview_imagens_cliente")
        }),
        ("Imagens geradas pela IA", {
            "fields": ("urls_imagens_sugeridas", "preview_imagens_sugeridas")
        }),
        ("Status e datas", {
            "fields": ("status", "criado_em", "atualizado_em")
        }),
    )

    # -------------------------
    # PREVIEW DE IMAGENS
    # -------------------------
    def preview_imagens_cliente(self, obj):
        return self._gallery(obj.imagens_cliente)
    preview_imagens_cliente.short_description = "Imagens enviadas pelo cliente"

    def preview_imagens_sugeridas(self, obj):
        return self._gallery(obj.urls_imagens_sugeridas)
    preview_imagens_sugeridas.short_description = "Imagens sugeridas pela IA"

    def _gallery(self, urls):
        if not urls:
            return "(nenhuma imagem)"

        html = ""
        for url in urls:
            html += f'<img src="{url}" width="80" style="margin:4px;border-radius:6px;border:1px solid #ddd;" />'
        return format_html(html)