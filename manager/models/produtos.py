from django.db import models
from os.path import splitext
from slugify import slugify
from django import forms
import secrets

# Gera um random hex no inicio do nome do arquivo


def upload_to_path(instance: 'ProdutoImagem', filename: str):
    hex = secrets.token_hex(64)
    return f'produtos/{hex}.{splitext(filename[:-1])}'


class Produto (models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, default='')
    slogan = models.CharField(max_length=100, blank=True, default='')
    descricao = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_lancamento = models.DateTimeField(
        'Data de Lançamento', blank=True, null=True)

    thumbnail = models.ImageField(upload_to=upload_to_path)
    imagens = models.ManyToManyField(
        'ProdutoImagem', blank=True, related_name='produto')

    categoria = models.ForeignKey(
        'Categoria', on_delete=models.CASCADE, null=True, blank=True)
    subcategoria = models.ForeignKey(
        'Subcategoria', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag')
    estoque = models.IntegerField(default=0)

    ativo = models.BooleanField(default=True)

    # Define um atributo padrão para um novo produto, para que o slug seja gerado a partir do nome
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def preco_liquido(self):
        return self.preco

    def desconto(self):
        return 10

    def __str__(self):
        return self.nome


class ProdutoImagem (models.Model):
    imagem = models.ImageField(upload_to=upload_to_path)


class Categoria (models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, default='')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    # Define um atributo padrão para um novo produto, para que o slug seja gerado a partir do nome
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Subcategoria (models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, default='')
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

    # Define um atributo padrão para um novo produto, para que o slug seja gerado a partir do nome
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Tag (models.Model):
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
