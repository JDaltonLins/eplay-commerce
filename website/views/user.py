
from django.shortcuts import render
from django.urls import path
from manager.models.produtos import Pedido

from manager.utils import required_login


def settings(req):
    pass


@required_login
def orders(req):
    return render(req, {
        'page': {
            'title': 'Meus pedidos - ePlay Commerce',
            'author': 'Dalton Lins e Jussara Kelly - Equipe ePlay Commerce',
        },
        'pedidos': Pedido.objects.filter(dono=req.user)
    })


urlpatterns = [
    path('user/settings', settings, name='user/settings'),
    path('user/orders', orders, name='user/orders')
]
