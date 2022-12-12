from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models

from principal.managers.usuario import UsuarioManager


class Usuario (AbstractUser, PermissionsMixin):
    imagem = models.ImageField(upload_to='usuarios', blank=True)
    color = models.CharField(max_length=6, default='000000')
    cargo = models.ForeignKey(
        'Cargo', on_delete=models.CASCADE, null=True, blank=True)

    objects = UsuarioManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.get_username()


class Cargo (models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    usuarios = models.ManyToManyField(
        Usuario, blank=True, related_name='cargo')

    def __str__(self):
        return self.nome
