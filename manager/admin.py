import inspect
import sys
from django.contrib import admin
from django.db.models import Model

from manager.models.produtos import *

# Register your models here.

# Pega todos os modelos do .models e registra no admin, dinamicamente

clsmembers = inspect.getmembers(sys.modules['manager.models'], inspect.isclass)
# Pega todo tipo de modelo que extende a classe Model e retorna somente os que não são abstratos, somente os validos

for name, cls in clsmembers:
    if issubclass(cls, Model) and not cls._meta.abstract and cls not in [Pedido, Produto, Categoria, Tag]:
        admin.site.register(cls)

# Teste


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'ativo')
    list_filter = ('ativo', 'categorias', 'tags')
    search_fields = ('nome', 'descricao')
    list_per_page = 20


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome',)
    list_per_page = 20


class TagAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome',)
    list_per_page = 20


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'user')
    list_filter = ('status', 'user')
    search_fields = ('nome',)
    list_per_page = 20


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Pedido, PedidoAdmin)
