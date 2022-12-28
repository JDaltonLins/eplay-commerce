
from django.shortcuts import redirect, render
from django.urls import path
from eplay_commerce.settings import MEDIA_URL
from manager.models.produtos import Pedido
from manager.models.usuario import Usuario

from website.forms.user import SettingsForm
from website.utils import build_meta

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET', 'POST'])
@login_required
def settings(req):
    if req.method == 'POST':
        form = SettingsForm(req.POST, req.FILES, instance=req.user)
        if form.is_valid():
            form.save()
            return redirect('user/settings')
    else:
        form = SettingsForm(instance=req.user)

    return render(req, 'user/config.html', {
        'page': build_meta('Configurações'),
        'form': form
    })


@require_http_methods(['GET'])
@login_required
def orders(req):
    pedidos = Pedido.objects.filter(user=req.user)
    return render(req, 'pedidos.html', {
        'page': build_meta('Pedidos', 'Pedidos realizados'),
        'pedidos': pedidos,
    })


urlpatterns = [
    path('user/configuracao', settings, name='user/settings'),
    path('user/pedidos', orders, name='user/orders')
]
