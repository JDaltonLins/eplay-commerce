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
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    mostrar_inicio = models.BooleanField(
        default=True, verbose_name='Mostrar na página inicial')
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

    categorias = models.ManyToManyField('Categoria', blank=False)
    tags = models.ManyToManyField('Tag', blank=True)
    estoque = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    # Define um atributo padrão para um novo produto, para que o slug seja gerado a partir do nome
    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def preco_liquido(self, desconto=0):
        preco = self.preco
        desconto = self.desconto() if desconto == 0 else desconto
        return desconto.calcular_preco(preco) if desconto else preco

    def desconto_preco(self, desconto=0):
        preco = self.preco
        desconto = self.desconto() if desconto == 0 else desconto
        return desconto.calcular(preco) if desconto else 0

    def porcentagem(self):
        desconto = self.desconto()
        return desconto.porcentagem(self) if desconto else 0

    def desconto(self):
        return PedidoDesconto.objects.procurar_desconto(self)


class ProdutoImagem (models.Model):
    imagem = models.ImageField(upload_to=upload_to_path)


class Categoria (models.Model):
    nome = models.CharField(max_length=100, unique=True)
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
    nome = models.CharField(max_length=100, unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    user = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    cupom = models.ForeignKey(
        'PedidoDesconto', on_delete=models.SET_NULL, null=True, blank=True)
    itens = models.ManyToManyField('PedidoItem')

    status = models.CharField(max_length=1, choices=[
        ('P', 'Pendente'), ('C', 'Cancelado'), ('S', 'Estornado'), ('E', 'Entregue')
    ], default='P')

    def __str__(self):
        return f'#{self.numero}'

    @property
    def numero(self):
        return f'{self.pk:06d}'

    def valor_total(self):
        if self.cupom:
            return self.valor - self.cupom.calcular(self.valor)
        else:
            return self.valor

    # Calcula todos os itens do pedido, e retorna o valor total
    def total(self):
        total, bruto, cupom, desconto = 0, 0, 0
        for item in self.itens.all():
            total += item.valor_total()
            bruto += item.produto.preco * item.quantidade
            desconto += item.produto.preco_liquido() * item.quantidade
            if item.cupom:
                cupom += item.cupom.calcular(item.produto.preco)


class PedidoItem(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.RESTRICT)
    quantidade = models.IntegerField(validators=[MinValueValidator(1)])
    desconto = models.ForeignKey(
        'PedidoDesconto', related_name='pedidos_descontos', null=True, blank=True, on_delete=models.RESTRICT)
    cupom = models.ForeignKey(
        'PedidoDesconto', related_name='pedidos_cupons', null=True, blank=True, on_delete=models.RESTRICT)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def valor_total(self):
        valor = self.produto.preco_liquido(self.desconto)
        if self.cupom:
            valor -= self.cupom.calcular(valor)
        return valor * self.quantidade

    def __str__(self):
        return f'{self.produto} - x{self.quantidade} - R$ {intcomma(self.valor_total(self.desconto))}'


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

    produtos = models.ManyToManyField('Produto', blank=True)
    categorias = models.ManyToManyField('Categoria', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    objects = PedidoDescontoManager()

    def calcular_preco(self, preco):
        return preco - self.calcular(preco)

    def calcular(self, valor):
        if self.tipo == 'P':
            return valor * (self.desconto / 100)
        else:
            return self.desconto

    def porcentagem(self, valor):
        if self.tipo == 'V':
            return self.desconto / valor * 100
        else:
            return self.desconto

    def aplicavel(self, produto):
        return (
            self.produtos.filter(id=produto.id).exists() or
            self.categorias.filter(id=produto.categoria.id).exists() or
            self.tags.filter(id__in=produto.tags.all()).exists()
        )

    # Ao salvar como Cupom e o codigo estiver em branco ele irá um código aleatório com hexadecimais
    def save(self, *args, **kwargs):
        if self.retorno == 'C' and not self.codigo:
            self.codigo = secrets.token_hex(3).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class CarrinhoItem (models.Model):
    user = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.produto} - x{self.quantidade}'

    @property
    def preco_bruto(self):
        return self.produto.preco * self.quantidade

    @property
    def preco_desconto(self):
        return self.produto.desconto().calcular(self.produto.preco) * self.quantidade if self.produto.desconto() else 0

    @property
    def total(self):
        return self.produto.preco_liquido() * self.quantidade

    class Meta:
        index_together = [
            ("user", "produto"),
        ]
