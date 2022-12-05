from django.utils import timezone
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse

from manager.models import Produto
from website.forms.produtos import FiltroProdutos
from website.utils import redirect_current, redirect_to

from django.db.models import Max


def produto(req: HttpRequest, produto_id: int, raw_slug: str = '') -> HttpResponse:
    try:
        produto = Produto.objects.get(id=produto_id)
        if produto.slug != raw_slug:
            return redirect_current(
                req, _args={"produto_id": produto_id, "raw_slug": produto.slug})

        # if produto.data_lancamento and produto.data_lancamento > timezone.now():
        #    return redirect_to(req, 'inicio')

        return render(req, 'produto.html', {'produto': produto})
    except Produto.DoesNotExist:
        return redirect('/')


def procurar(req: HttpRequest) -> HttpResponse:
    print(req.POST)
    form = FiltroProdutos(req.POST or None)
    if form.is_valid():
        produtos = form.search()
    else:
        produtos = Produto.objects.all()

    paginas = Produto.objects.all().count() // 10 + 1

    return render(req, 'produtos.html', {
        "form": form,
        "produtos": produtos,
        "paginas": paginas,
    })
