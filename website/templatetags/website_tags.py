from django import template

from website.utils import _contact_dicts, build_url

register = template.Library()


@register.simple_tag(name='redirect_to')
def redirect_to_tag(page, **params):
    if 'props' in params:
        props = params['props']
        del params['props']
    else:
        props = {}
    return build_url(page, args=props, search_params=params)


@register.simple_tag(name='redirect_current', takes_context=True)
def redirect_current_tag(context, **params):
    params = _contact_dicts(context.request.GET.dict(), params)
    return redirect_to_tag(context.request.resolver_match.view_name, **params)
