from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse

from manager.models import Produto
from website.forms.produtos import PesquisaProdutos
from website.utils import redirect_current

from django.db.models import Max


def produto(req: HttpRequest, produto_id: int, raw_slug: str = '') -> HttpResponse:
    try:
        produto = Produto.objects.get(id=produto_id)
        if produto.slug != raw_slug:
            return redirect_current(
                req, _args={"produto_id": produto_id, "raw_slug": produto.slug})

        return render(req, 'produto.html', {'produto': produto})
    except Produto.DoesNotExist:
        return redirect('/')


def procurar(req: HttpRequest) -> HttpResponse:
    form = PesquisaProdutos(req.GET)
    if form.is_valid():
        produtos = form.search()
    else:
        produtos = Produto.objects.all()

    max = Produto.objects.all().aggregate(Max('preco'))['preco__max']
    max = (max // 10 + 1) * 10

    paginas = Produto.objects.all().count() // 10 + 1

    return render(req, 'produtos.html', {
        "form": form,
        "produtos": produtos,
        "max": max,
        "paginas": paginas,
    })
