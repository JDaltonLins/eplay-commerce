from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static
from eplay_commerce.settings import MEDIA_URL

from painel.urls import urlpatterns as painel_urls
from website.urls import urlpatterns as website_urls
from manager.views import on_verify_email

urlpatterns = [
    path('email/<str:template>/', lambda req, template: render(req,
         'email/' + template + '.html', {'usuario': {'nome': 'Dalton Lins'}, 'confirmacao': {'ip': '127.0.0.129', 'user_agent': 'Chrome', 'system': 'Windows 8', 'country_code': 'BR', 'country_name': 'Brasil'}})),
    path('auth/verify/<str:type>/<str:token>/<str:uid>', on_verify_email),
    path('admin/', admin.site.urls),
    path('painel/', include(painel_urls)),
] + website_urls


if settings.DEBUG:
    urlpatterns += [re_path('^' + MEDIA_URL + 'usuarios/usuarios-default.svg$',
                            lambda req: redirect('/static/img/usuarios-default.svg'))]
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    # handler400 = 'website.views.error.bad_request'
    # handler403 = 'website.views.error.permission_denied'
    # handler404 = 'website.views.error.not_found'
    # handler500 = 'website.views.error.server_error'
    pass
