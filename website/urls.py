from django.urls import path, include
from django.shortcuts import render, redirect
from django.urls import reverse

from website.views.produtos import produto

urlpatterns = [
    path('/', render, {'template_name': 'index.html'}, name='index'),
    path('categorias/', render, {'template_name': 'categorias.html'}),
    path('categorias/<int:categoria_id>/', render,
         {'template_name': 'categoria.html'}),
    path('produto/', redirect, {'to': '/'}),
    path('produto/<int:produto_id>-<slug:raw_slug>', produto, name='produto'),
    path('produto/<int:produto_id>', produto, name='produto'),
    path('view/', render, {'template_name': 'content/content.html'}),
]
