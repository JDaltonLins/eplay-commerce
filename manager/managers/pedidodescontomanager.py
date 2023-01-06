

from django.db import models
from django.utils import timezone
from django.db.models import Q

from django.core import serializers

class PedidoDescontoManager (models.Manager):

    def procurar_cupom(self, codigo):
        # Puxa se o produto está em alguma categoria, subcategoria ou tag que tenha um desconto
        descontos = self.filter(
            ativo=True,
            retorno='C',
            codigo=codigo
        ).filter(
            Q(inicio__lte=timezone.now()) | Q(inicio__isnull=True),
            Q(fim__gte=timezone.now()) | Q(fim__isnull=True)
        )

        return descontos.first()

    def procurar_desconto(self, produto):
        # Puxa se o produto está em alguma categoria, subcategoria ou tag que tenha um desconto
        descontos = self.filter(
            retorno='P',
            ativo=True
        ).filter(
            Q(inicio__lte=timezone.now()) | Q(inicio__isnull=True),
            Q(fim__gte=timezone.now()) | Q(fim__isnull=True)
        ).filter(
            Q(categorias__in=produto.categorias.all()) |
            Q(tags__in=produto.tags.all()) |
            Q(produtos__in=[produto])
        )

        # Através do SQL, ele irá gerar uma coluna chamada 'calculado' que terá a seguinte condição
        # > Se a coluna 'tipo' for 'P' (porcentagem), ele irá calcular o desconto em porcentagem
        # > Se a coluna 'tipo' for 'V' (valor), ele irá calcular o desconto em valor

        descontos = descontos.annotate(
            calculado=models.Case(
                models.When(tipo='P', then=models.F(
                    'desconto') * produto.preco / 100),
                models.When(tipo='V', then=models.F('desconto')),
                default=0,
                output_field=models.DecimalField()
            )
        )

        descontos = descontos.order_by('-calculado')

        desconto = descontos.first()

        return desconto if desconto else None
