from django.urls import path
from manager.utils import required_login


def carrinho(req):
    pass


def validar(req):
    pass


urlpatterns = [
    path('carrinho/', carrinho, name='carrinho'),
]
