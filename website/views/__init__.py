
from django.shortcuts import render

from django.db.models import Count
from manager.models.produtos import Categoria, Produto


def render_index(req):
    return render(req, 'index.html', {
        "pagina":
        {
            "titulo": "Inicio - ePlay Commerce",
            "descricao": "Página inicial da ePlay Commerce",
            "atual": "inicio",
            "tags": ["games", "jogos", "loja", "store", "eplay", "eplay commerce"]
        },
        "produtos": Produto.objects.filter(ativo=True, mostrar_inicio=True).order_by('created_at')[:5],
        # Mostra apenas as categorias que possuem produtos, estão ativas e com a opção Mostrar_Inicio = True
        "categorias": Categoria.objects.filter(ativo=True, mostrar_inicio=True, produto__isnull=False).order_by(
            'created_at', 'nome').distinct()[:5]
    })
