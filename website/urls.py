from django.urls import path, include
from django.shortcuts import render, redirect
from django.urls import reverse

from website.views.produtos import produto, procurar
from website.views.auth import urlpatterns as auth_patterns
from website.views.carrinho import urlpatterns as carrinho_patterns
from website.views.produtos import urlpatterns as produtos_patterns
from website.views.user import urlpatterns as user_patterns

from website.views import render_index, render_sobrenos
urlpatterns = [
    path('', render_index, name='home'),
    path('/sobre-nos/', render_sobrenos, name='sobre-nos'),
] + auth_patterns + produtos_patterns + carrinho_patterns + user_patterns
