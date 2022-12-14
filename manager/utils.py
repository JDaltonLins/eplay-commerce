from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from json import loads


def json(func):
    def wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            return response
        return JsonResponse(response)
    return wrapper


def login_requirement(func, required=True):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated != required:
            return HttpResponse(status=401)
        return func(request, *args, **kwargs)
    return wrapper


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
            body = loads(request.body)
            kwargs.update({param: body[param] for param in params})
            try:
                return func(request, *args, **kwargs)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        return wrapper
    return decorator
