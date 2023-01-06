
from django.shortcuts import render

from django.db.models import Count
from manager.models.produtos import Categoria, Produto
from website.utils import build_meta


def render_index(req):
    return render(req, 'index.html', {
        "page": build_meta('Inicio'),
        "produtos": Produto.objects.filter(ativo=True, mostrar_inicio=True).order_by('created_at')[:5],
        # Mostra apenas as categorias que possuem produtos, estão ativas e com a opção Mostrar_Inicio = True
        "categorias": Categoria.objects.filter(ativo=True, mostrar_inicio=True, produto__isnull=False).order_by(
            'created_at', 'nome').distinct()[:5]
    })


def render_sobrenos(req):
    return render(req, 'sobre-nos.html', {
        'page': build_meta("Sobre nós", "Sobre nós", "sobrenos", ["sobre", "nós", "eplay", "eplay commerce"])
    })
