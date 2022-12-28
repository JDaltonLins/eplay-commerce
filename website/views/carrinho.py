import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.urls import path
from django.db import transaction
from manager.models.produtos import CarrinhoItem, Pedido, PedidoItem
from website.forms.carrinho import CarrinhoAction, CarrinhoFinalizar
from website.utils import build_meta

from django.contrib.auth.decorators import login_required


@require_http_methods(['GET'])
@login_required
def carrinho(req):
    items = CarrinhoItem.objects.filter(user=req.user)
    total, preco_bruto, preco_desconto = 0, 0, 0
    qntd = 0

    for item in items:
        total += item.produto.preco_liquido()
        preco_bruto += item.produto.preco
        preco_desconto += item.produto.desconto_preco()

    return render(req, 'carrinho.html', {
        'page': build_meta('Carrinho', 'Carrinho de compras'),
        'itens': items,
        'info': {
            'total': {
                'bruto': preco_bruto,
                'desconto': preco_desconto,
                'liquido': total
            },
            'quantidade': qntd,
            'items': len(items),
        }
    })


@require_http_methods(['POST'])
@login_required
def finalizar(req):
    carrinho = CarrinhoFinalizar(req.POST)
    if not carrinho.is_valid():
        return JsonResponse(carrinho.errors, status=400)
    try:
        with transaction.atomic():
            items = CarrinhoItem.objects.filter(user=req.user)
            cupom = carrinho.cleaned_data['cupom']

            pedido = Pedido(
                user=req.user
            )

            for item in items:
                produto = item.produto
                if produto.estoque < item.quantidade:
                    return JsonResponse({'status': 'error', 'message': f'{produto.nome} só tem {produto.estoque} unidades disponíveis, favor remontar seu carrinho.'}, status=400)

                pedido_item = PedidoItem.objects.create(
                    produto=item.produto,
                    quantidade=item.quantidade,
                    desconto=item.produto.desconto(),
                    cupom=cupom if cupom and cupom.aplicavel(
                        item.produto) else None
                )
                pedido_item.save()
                pedido.itens.add(pedido_item)

            items.delete()
            pedido.save()

            return JsonResponse({'status': 'success'})
    except:
        return JsonResponse({'status': 'error', 'message': 'Erro ao finalizar compra'}, status=400)


@require_http_methods(['POST'])
@login_required
def add_carrinho(req):
    carrinho = CarrinhoAction(json.loads(req.body))
    if not carrinho.is_valid():
        return JsonResponse(carrinho.errors, status=400)
    return JsonResponse(carrinho.save(req.user))


@require_http_methods(['POST'])
@login_required
def remover_carrinho(req):
    carrinho = CarrinhoAction(json.loads(req.body))
    if not carrinho.is_valid():
        return JsonResponse(carrinho.errors, status=400)

    return JsonResponse(carrinho.delete(req.user))


@require_http_methods(['POST'])
@login_required
def clear_carrinho(req):
    CarrinhoItem.objects.filter(user=req.user).delete()
    return JsonResponse({
        'status': 'success',
    })


urlpatterns = [
    path('carrinho/', carrinho, name='carrinho'),
    path('api/carrinho/finalizar', finalizar, name='carrinho/finalizar'),
    path('api/carrinho/add', add_carrinho, name='carrinho/add'),
    path('api/carrinho/rem', remover_carrinho, name='carrinho/remover'),
    path('api/carrinho/clear', clear_carrinho, name='carrinho/limpar'),
]
