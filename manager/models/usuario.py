from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models

from manager.managers.usuario import UsuarioManager
import random
import string

from manager.managers.usuario import UsuarioManager
from manager.managers.usuario_confirmacao import UsuarioConfirmacaoManager
from manager.utils import random_token, random_uid


class Usuario (AbstractUser, PermissionsMixin):
    imagem = models.ImageField(upload_to='usuarios', blank=True)
    color = models.CharField(max_length=6, default='000000')
    cargo = models.ForeignKey(
        'Cargo', on_delete=models.CASCADE, null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    objects = UsuarioManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.get_username()


class UsuarioConfirmacao (models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='confirmacoes')
    token = models.CharField(max_length=100, default=random_token)
    uid = models.CharField(max_length=64, default=random_uid)
    type = models.CharField(max_length=10)
    data = models.DateTimeField(auto_now_add=True)

    object = UsuarioConfirmacaoManager()


class Cargo (models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome
