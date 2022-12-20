from django.urls import path, reverse
from django.utils import timezone
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse

from manager.models import Produto
from manager.models.produtos import Categoria
from website.forms.produtos import FiltroProdutos
from website.utils import build_meta, redirect_current, redirect_to

from django.db.models import Max
from django.core.paginator import Paginator
from django.contrib.humanize.templatetags.humanize import intcomma

import json


def produto(req: HttpRequest, produto_id: int, raw_slug: str = '') -> HttpResponse:
    try:
        produto = Produto.objects.get(ativo=True, id=produto_id)

        if produto.slug != raw_slug:
            return redirect_current(
                req, _args={"produto_id": produto_id, "raw_slug": produto.slug})

        if produto.data_lancamento and produto.data_lancamento > timezone.now() and not (req.user and req.user.is_staff):
            return redirect_to(req, 'inicio')

        return render(req, 'produto.html', {
            'page': {
                'title': f"{produto.nome} - ePlay Commerce",
                'description': produto.descricao,
                'keywords': [*produto.tags.all().values_list('nome', flat=True), *produto.categorias.all().values_list('nome', flat=True)],
                'author': 'Dalton Lins, Jussara Kelly - Equipe ePlay Commerce'
            },
            'produto': produto,
            'produto_meta': json.dumps({
                "@context": "https://schema.org",
                "@type": "Product",
                'sku': produto.id,
                'name': produto.nome,
                'description': produto.descricao,
                'imagem': f"{req.scheme}://{req.get_host()}{produto.thumbnail.url}",
                "offers": {
                    "@type": "Offer",
                    "availability": "https://schema.org/InStock",
                    "price": intcomma(produto.preco),
                    "priceCurrency": "BRL",
                    "url": f"{req.scheme}://{req.get_host()}{reverse('produto', kwargs={'produto_id': produto.id, 'raw_slug': produto.slug})}"
                }
            })
        })
    except Produto.DoesNotExist:
        return redirect('/')


def procurar(req: HttpRequest) -> HttpResponse:
    form = FiltroProdutos(req.GET or None)
    if form.is_valid():
        produtos = form.search()
    else:
        produtos = Produto.objects.all()

    produtos = produtos if req.user and req.user.is_staff else produtos.filter()
    paginacao = Paginator(produtos, 16)

    try:
        paginacao = paginacao.page(form.cleaned_data.get('pagina', 1))
    except:
        paginacao = paginacao.page(1)

    return render(req, 'produtos.html', {
        "page": build_meta('Pesquisa de Produtos'),
        "form": form,
        "paginacao": paginacao
    })


def categorias(req):
    return render(req, 'categorias.html', {
        'page': build_meta('Categorias'),
        'categorias': Categoria.objects.filter(ativo=True, produto__isnull=False)
    })


urlpatterns = [
    path('produto/', procurar, name='produtos'),
    path('produto/<int:produto_id>-<slug:raw_slug>', produto, name='produto'),
    path('produto/<int:produto_id>', produto, name='produto'),
    path('categorias/', categorias, name='categorias')
]
