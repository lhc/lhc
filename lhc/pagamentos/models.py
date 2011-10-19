#-*- coding: utf-8 -*-
from django.db import models
from associados.models import Associado

# Create your models here.
class Pagamento(models.Model):
    data = models.DateField()
    valor = models.DecimalField(decimal_places=3, max_digits=50)
    descricao = models.CharField(max_length=100)

    # TODO gostaria de o acoplamento não fosse acoplado
    # com um associado e sim com qualquer model que o 
    # desenvolvedor quiser.
    associado = models.ForeignKey(Associado)

    def __unicode__(self):
        return '%s - %s - %s - %s' % (self.associado, self.data, self.valor, self.descricao)
