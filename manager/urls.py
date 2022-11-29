from django.contrib import admin
from django.urls import path, include

from painel.urls import urlpatterns as painel_urls
from website.urls import urlpatterns as website_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('painel/', include(painel_urls)),
] + website_urls

