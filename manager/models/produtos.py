from django.db import models
from os.path import splitext
from slugify import slugify


def upload_to_path(instance: 'Produto', filename: str):
    return f'produtos/{instance.slug}.{splitext(filename[1])}'


class Produto (models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    descricao = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to=upload_to_path)
    ativo = models.BooleanField(default=True)

    categoria = models.ForeignKey(
        'Categoria', on_delete=models.CASCADE, null=True, blank=True)
    subcategoria = models.ForeignKey(
        'Subcategoria', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag')

    estoque = models.IntegerField(default=0)

    # Define um atributo padrão para um novo produto, para que o slug seja gerado a partir do nome
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Categoria (models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Subcategoria (models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Tag (models.Model):
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
