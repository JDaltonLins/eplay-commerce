

from django.db import models
from django.utils import timezone
from django.db.models import Q


class PedidoDescontoManager (models.Manager):

    def procurar_cupom(self, codigo):
        return self.get_queryset().filter(ativo=True, retorno='C', codigo=codigo).filter(
            Q(inicio__lte=timezone.now()) | Q(inicio=None),
            Q(fim__gte=timezone.now()) | Q(fim=None)
        ).first()

    def procurar_desconto(self, produto):
        return self.get_queryset().filter(ativo=True, retorno='P').filter(
            Q(inicio__lte=timezone.now()) | Q(inicio=None),
            Q(fim__gte=timezone.now()) | Q(fim=None)
        ).filter()
