from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from painel.urls import urlpatterns as painel_urls
from website.urls import urlpatterns as website_urls
from manager.views import on_verify_email

urlpatterns = [
    path('email/<str:template>/', lambda req, template: render(req,
         'email/' + template + '.html', {'usuario': {'nome': 'Dalton Lins'}})),
    path('auth/verify/<str:type>/<str:token>/<str:uid>', on_verify_email),
    #    path('admin/', admin.site.urls),
    #    path('painel/', include(painel_urls)),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
