from django.urls import path, include
from django.shortcuts import render, redirect
from django.urls import reverse

from website.views.produtos import produto, procurar

urlpatterns = [
    path('', render, {'template_name': 'index.html'}, name='inicio'),
    path('categorias/', render,
         {'template_name': 'categorias.html'}, name='categorias'),
    path('categorias/<int:categoria_id>/', render,
         {'template_name': 'categoria.html'}),
    path('produto/', procurar, name='produtos'),
    path('produto/<int:produto_id>-<slug:raw_slug>', produto, name='produto'),
    path('produto/<int:produto_id>', produto, name='produto'),
    path('promocoes/', render,
         {'template_name': 'promocoes.html'}, name='promocoes'),
]
