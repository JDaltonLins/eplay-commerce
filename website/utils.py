from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode


def _contact_dicts(dic1, dic2):
    for key, value in dic2.items():
        if value is None or value == '':
            del dic1[key]
        else:
            dic1[key] = value
    return dic1

def build_meta(title, description=None, keyworks=None, author='Dalton Lins e Jussara Kelly - Equipe ePlay Commerce'):
    return {
        'title': f'{title} - ePlay Commerce',
        'description': description,
        'keywords': keyworks,
        'author': author
    }

def build_url(page, args=None, search_params={}):
    new_dic = {}
    for key, value in search_params.items():
        if not (value is None or value == ''):
            new_dic[key] = value

    return f'{reverse(page, kwargs=args)}?{urlencode(new_dic)}' if new_dic else reverse(page, kwargs=args)


def redirect_to(req: HttpRequest, page, **extra_fields):
    search_params = _contact_dicts(req.GET.dict(), extra_fields) if req else {} if req else {}

    page, args = page if type(page) in (list, tuple) else (page, [])

    return redirect(build_url(page, args, search_params))


def redirect_current(req: HttpRequest, **extra_fields):
    page = req.resolver_match.view_name
    if '_args' in extra_fields:
        args = extra_fields['_args']
        del extra_fields['_args']
    else:
        args = []

    return redirect_to(req, (page, args), **extra_fields)
