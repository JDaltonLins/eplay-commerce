from django.shortcuts import render
from website.utils import build_meta


def not_found(req, exception=None):
    return render(req, 'website:error/generic.html', {
        'page': build_meta('404', 'Página não encontrada'),
        'error': '404',
        'message': 'Página não encontrada',
        'exception': exception or 'Erro desconhecido'
    })


def server_error(req, exception=None):
    return render(req, 'error/generic.html', {
        'page': build_meta('500', 'Erro interno'),
        'error': '500',
        'message': 'Erro interno',
        'exception': exception or 'Erro desconhecido'
    })


def permission_denied(req, exception=None):
    return render(req, 'error/generic.html', {
        'page': build_meta('403', 'Acesso negado'),
        'error': '403',
        'message': 'Acesso negado',
        'exception': exception or 'Erro desconhecido'
    })


def bad_request(req, exception=None):
    return render(req, 'error/generic.html', {
        'page': build_meta('400', 'Requisição inválida'),
        'error': '400',
        'message': 'Requisição inválida',
        'exception': exception or 'Erro desconhecido'
    })


def csrf_failure(req, reason=''):
    return render(req, 'error/generic.html', {
        'page': build_meta('403', 'Acesso negado'),
        'error': '403',
        'message': 'Acesso negado\n\n' + reason
    })
