
from django.shortcuts import render

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
        "categorias": Categoria.objects.filter(ativo=True, mostrar_inicio=True).order_by('created_at', 'nome')[:5]
    })
