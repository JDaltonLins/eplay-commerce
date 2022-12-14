from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from painel.urls import urlpatterns as painel_urls
from website.urls import urlpatterns as website_urls

urlpatterns = [
    path('email/<str:template>/', lambda req, template: render(req,
         'email/' + template + '.html', {'usuario': {'nome': 'Dalton Lins'}, 'confirmacao': {'ip': '127.0.0.129', 'user_agent': 'Chrome', 'system': 'Windows 8', 'country_code': 'BR', 'country_name': 'Brasil'}})),
    path('admin/', admin.site.urls),
    path('painel/', include(painel_urls)),
] \
    + website_urls \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
