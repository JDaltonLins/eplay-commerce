
from django.shortcuts import redirect, render
from django.urls import path
from eplay_commerce.settings import MEDIA_URL
from manager.models.produtos import Pedido
from manager.models.usuario import Usuario

from manager.utils import required_login
from website.forms.user import SettingsForm
from website.utils import build_meta


def settings(req):
    if req.method == 'POST':
        form = SettingsForm(req.POST, req.FILES, instance=req.user)
        if form.is_valid():
            form.save()
            return redirect('user/settings')
    else:
        form = SettingsForm(instance=req.user)

    return render(req, {
        'page': build_meta('Configuarações'),
        'form': form
    })


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
