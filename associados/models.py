#-*- coding: utf-8 -*-
from django.db import models

class Associado(models.Model):
    nome = models.CharField(max_length=100)
    apelido = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=12, blank=True, null=True)

    valor_mensalidade = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __unicode__(self):
        if self.apelido and self.nome:
            return '%s (%s)' % (self.nome, self.apelido)
        return self.nome or self.apelido
