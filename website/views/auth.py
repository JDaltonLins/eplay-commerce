from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.urls import path
from manager.models.usuario import UsuarioConfirmacao
from manager.utils import required_login
from website.forms.auth import ChangeEmailForm, LoginForm, RegistrarForm
from django.contrib.auth import authenticate, login as login_django, logout as logout_django

from website.utils import build_url, redirect_to
from urllib.parse import urlsplit


@require_http_methods(['GET', 'POST'])
def login(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is None:
                form.add_error('username', 'Usuário ou senha inválidos')
                form.add_error('password', 'Usuário ou senha inválidos')
            login_django(req, user)
            if not user.is_active or not user.email_verified:
                return redirect_to(req, 'auth/info')
            else:
                url_next = req.GET.get('next', None)
                if url_next is not None:
                    parsed = urlsplit(url_next)
                    if parsed and parsed.netloc == req.get_host():
                        return redirect_to(req, url_next)
                    else:
                        return redirect_to(req, url_next)
                elif user.is_staff:
                    return redirect_to(req, 'painel/home')
                else:
                    return redirect_to(req, 'home')
    else:
        form = LoginForm()

    return render(req, 'auth/login.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def registrar(req):
    if req.method == 'POST':
        form = RegistrarForm(req.POST)
        if form.is_valid():
            # Irá tentar registrar o usuário
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect_to(req, 'auth/login')
    else:
        form = RegistrarForm()

    return render(req, 'auth/registrar.html', {'form': form})


@require_http_methods(['GET'])
def info(req):
    print(req.user, req.user.id)
    if req.user is None or req.user.is_anonymous:
        return redirect_to(req, 'auth/login')
    elif not req.user.is_active:
        return render(req, 'auth/aviso.html', {
            'page': {
                'title': 'Usuário desativado - ePlay Commerce'
            },
            'message': 'O seu usuário está desativado.\nEntre em contato com o administrador do sistema',
        })
    elif not req.user.email_verified:
        return render(req, 'auth/aviso.html', {
            'page': {
                'title': 'Email não verificado - ePlay Commerce'
            },
            'message': 'O seu e-mail ainda não foi verificado.\nVerifique sua caixa de entrada ou spam e tente novamente\n\nCaso não tenha recebido o e-mail, clique no botão abaixo para reenviar ou trocar de e-mail',
            'button': {
                'text': 'Redefinir e-mail',
                'url': build_url('auth/change-email')
            }
        })
    else:
        return redirect_to(req, 'home')


@require_http_methods(['GET', 'POST'])
@required_login(required_email=False)
def change_email(req):
    if req.method == 'POST':
        form = ChangeEmailForm(req.POST)
        if form.is_valid():
            req.user.email = form.cleaned_data['email']
            req.user.save()

            result = UsuarioConfirmacao.objects.send_confirmation_email(
                req, req.user, 'email')
            if result is None:
                return render(req, 'auth/aviso.html', {
                    'message': 'Ocorreu um erro ao enviar o e-mail de confirmação.\nTente novamente ou entre em contato com o administrador do sistema',
                })
            elif result is True:
                return render(req, 'auth/aviso.html', {
                    'message': 'O e-mail foi alterado com sucesso!\nFaça o login novamente para utilizar o novo e-mail',
                })
            else:
                return redirect_to(req, 'auth/login')
    else:
        form = ChangeEmailForm()

    return render(req, 'auth/change-email.html', {'form': form})


@require_http_methods(['GET'])
def confirm_token(req, token, uid):
    if UsuarioConfirmacao.objects.verify(token, uid):
        return redirect_to(req, 'auth/login')
    else:
        return render(req, 'auth/aviso.html', {
            'page': {
                'title': 'Token inválido - ePlay Commerce'
            },
            'message': 'O token informado é inválido ou expirou.\nTente novamente ou entre em contato com o administrador do sistema',
        })


@require_http_methods(['GET'])
@required_login(required_email=False)
def logout(req):
    logout_django(req)
    return redirect_to(req, 'auth/login')


urlpatterns = [
    path('auth/info/', info, name='auth/info'),
    path('auth/logout/', logout, name='auth/logout'),
    path('auth/login/', login, name='auth/login'),
    path('auth/registrar/', registrar, name='auth/register'),
    path('auth/redefinir-email/', change_email, name='auth/change-email'),
    path('auth/confirmar/<str:token>/<str:uid>/',
         confirm_token, name='auth/confirm-token')
]
