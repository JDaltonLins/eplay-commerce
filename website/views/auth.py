from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.urls import path, include
from website.forms.auth import LoginForm, RegistrarForm


@require_http_methods(['GET', 'POST'])
def login(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
    else:
        form = LoginForm()

    return render(req, 'auth/login.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def registrar(req):
    if req.method == 'POST':
        form = RegistrarForm(req.POST)
    else:
        form = RegistrarForm()

    return render(req, 'auth/registrar.html', {'form': form})


urlpatterns = [
    path('auth/login/', login, name='auth/login'),
    path('auth/registrar/', registrar, name='auth/register'),
]
