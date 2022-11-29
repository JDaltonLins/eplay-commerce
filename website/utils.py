from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode


def redirect_to(req: HttpRequest, page, **extra_fields):
    search_params = req.GET.dict() if req else {}

    for key, value in extra_fields.items():
        if value is None:
            del search_params[key]
        else:
            search_params[key] = value

    page, args = page if type(page) in (list, tuple) else (page, [])

    return redirect(f'{reverse(page, kwargs=args)}?{urlencode(search_params)}' if search_params else reverse(page, kwargs=args))


def redirect_current(req: HttpRequest, **extra_fields):
    page = req.resolver_match.view_name
    if '_args' in extra_fields:
        args = extra_fields['_args']
        del extra_fields['_args']
    else:
        args = []

    return redirect_to(req, (page, args), **extra_fields)
