from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

import json
import random
import string

from website.utils import redirect_to


def delete_all_unexpired_sessions_for_user(user):
    unexpired_sessions = Session.objects.filter(
        expire_date__gte=timezone.now())
    [
        session.delete() for session in unexpired_sessions
        if str(user.pk) == session.get_decoded().get('_auth_user_id')
    ]


def json(func):
    def wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            return response
        return JsonResponse(response)
    return wrapper


def required_login(required=True, required_email=True, redirect=None):
    
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated != required or (required_email and not request.user.email_verified):
                return HttpResponse(status=401) # redirect_to(request, **redirect) if redirect else HttpResponse(status=401)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def login_required(required=True, required_email=True, redirect='auth/login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated == required and (not required_email or u.email_verified),
        login_url=redirect_to(None, **redirect),
        redirect_field_name=REDIRECT_FIELD_NAME,
    )
    return actual_decorator

def admin_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return HttpResponse(status=401)
        return func(request, *args, **kwargs)
    return wrapper


def body_params(*params):
    """
        Extrai os parametros do corpo da requisição para a função
        Exemplo:

        Exemplo de requisição:
        POST /api/func
        BODY {
            name: 'func',
            age: 20
        }

        Exemplo de função:
        @body_params()
        def func(request, name, age):
            pass
    """
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method not in ['POST', 'PUT']:
                return HttpResponseNotAllowed(['POST', 'PUT'])
            body = json.loads(request.body)
            kwargs.update({param: body[param] for param in params})
            try:
                return func(request, *args, **kwargs)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        return wrapper
    return decorator


def random_token(size=100):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


def random_uid():
    ''.join(random.choice(string.hexdigits) for _ in range(32))
