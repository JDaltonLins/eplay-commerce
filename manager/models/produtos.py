from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils import timezone
from os.path import splitext
from django.core.validators import MinValueValidator, MinLengthValidator
from django.contrib.humanize.templatetags.humanize import intcomma

import secrets

from manager.managers.pedidodescontomanager import PedidoDescontoManager


def upload_to_path(instance: 'ProdutoImagem', filename: str):
    hex = secrets.token_hex(64)
    return f'/static/produtos/{hex}.{splitext(filename)}'


class Produto (models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, default='')
    slogan = models.CharField(max_length=100, blank=True, default='')
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_lancamento = models.DateTimeField(
        'Data de Lançamento', blank=True, null=True)

    thumbnail = models.ImageField(upload_to=upload_to_path)
    imagens = models.ManyToManyField(
        'ProdutoImagem', blank=True, related_name='produto')

    categorias = models.ManyToManyField('Categoria')
    tags = models.ManyToManyField('Tag')
    estoque = models.IntegerField(default=0)

    ativo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    mostrar_inicio = models.BooleanField(default=True)

    # Define um atributo padrão para um novo produto, para que o slug seja gerado a partir do nome
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def desconto(self):
        # Verifica se há algum desconto com o PedidoDesconto aplicado ao produto ou então se há um desconto padrão
        desconto = PedidoDescontoProduto.objects.filter(
            produto=self,
            desconto__ativo=True,
        ).filter(
            Q(desconto__inicio__lte=timezone.now()) | Q(
                desconto__inicio__isnull=True),
            Q(desconto__fim__gte=timezone.now()) | Q(
                desconto__fim__isnull=True)
        )
        # Raw query para verificar se há algum desconto com o PedidoDesconto aplicado ao produto ou então se há um desconto padrão
        if not desconto:
            descontos = PedidoDesconto.objects.filter(
                ativo=True
            ).filter(
                Q(inicio__lte=timezone.now()) | Q(
                    inicio__isnull=True),
                Q(fim__gte=timezone.now()) | Q(
                    fim__isnull=True)
            ).filter(pedidodescontotag__id__in=(0, 1, 2, 3)) \
                .filter(pedidodescontocategoria__id__in=(0, 1, 2, 3)) \
                .filter(pedidodescontosubcategoria__id__in=(0, 1, 2, 3)) \
                .filter(pedidodescontoproduto__id__in=(0, 1, 2, 3))

            for desconto in descontos:
                if not desconto.pedidodescontoproduto_set.filter(produto=self.categoria).exists():
                    return desconto.desconto

    def preco_liquido(self):
        return float(self.preco) * 0.9

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
    mostrar_inicio = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    # Define um atributo padrão para um novo produto, para que o slug seja gerado a partir do nome
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Tag (models.Model):
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    cupom = models.ForeignKey(
        'PedidoDesconto', on_delete=models.SET_NULL, null=True, blank=True)
    itens = models.ManyToManyField('PedidoItem')

    dono = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    status = models.CharField(max_length=1, choices=[
        ('P', 'Pendente'), ('C', 'Cancelado'), ('S', 'Estornado'), ('E', 'Entregue')
    ])

    def __str__(self):
        return f'#{self.numero}'

    @property
    def numero(self):
        return f'{self.id:06d}'

    def valor_total(self):
        if self.desconto:
            return self.valor - self.desconto.calcular(self.valor)
        else:
            return self.valor


class PedidoItem(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.RESTRICT)
    quantidade = models.IntegerField(validators=[MinValueValidator(1)])
    desconto = models.ForeignKey(
        'PedidoDescontoProduto', null=True, blank=True, on_delete=models.RESTRICT)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def valor_total(self):
        return self.valor * self.quantidade

    def __str__(self):
        return f'{self.produto} - x{self.quantidade} - R$ {intcomma(self.valor_total())}'


class PedidoDesconto(models.Model):
    ativo = models.BooleanField(default=True)
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, blank=True, default='', validators=[
                              MinLengthValidator(5)], db_index=True)
    tipo = models.CharField(
        max_length=1, choices=[('P', 'Porcentagem'), ('V', 'Valor')])
    retorno = models.CharField(
        max_length=1, choices=[('P', 'Promoção'), ('C', 'Cupom')], db_index=True)
    inicio = models.DateTimeField(blank=True, null=True, db_index=True)
    fim = models.DateTimeField(blank=True, null=True, db_index=True)
    desconto = models.DecimalField(max_digits=10, decimal_places=2)

    produtos = models.ManyToManyField(
        'Produto', through='PedidoDescontoProduto')
    categorias = models.ManyToManyField(
        'Categoria', through='PedidoDescontoCategoria')
    tags = models.ManyToManyField('Tag', through='PedidoDescontoTag')

    objects = PedidoDescontoManager()

    def calcular(self, valor):
        if self.tipo == 'P':
            return valor * (self.desconto / 100)
        else:
            return self.desconto

    def procentagem(self, valor):
        if self.tipo == 'V':
            return self.desconto / valor * 100
        else:
            return self.desconto

    # Ao salvar como Cupom e o codigo estiver em branco ele irá um código aleatório com hexadecimais
    def save(self, *args, **kwargs):
        if self.retorno == 'C' and not self.codigo:
            self.codigo = secrets.token_hex(3).upper()
        super().save(*args, **kwargs)


class PedidoDescontoTag(models.Model):
    pedidodesconto = models.ForeignKey(
        'PedidoDesconto', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)


class PedidoDescontoCategoria(models.Model):
    pedidodesconto = models.ForeignKey(
        'PedidoDesconto', on_delete=models.CASCADE)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)


class PedidoDescontoProduto(models.Model):
    pedidodesconto = models.ForeignKey(
        'PedidoDesconto', on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
