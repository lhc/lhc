#-*- coding: utf-8 -*-
from django.db import models

class Associado(models.Model):
    nome = models.CharField(max_length=100)
    apelido = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=12, null=True)

    valor_mensalidade = models.DecimalField(decimal_places=4, max_digits=10)
    ativo = models.BooleanField(default=True)

    def __unicode__(self):
        if self.apelido and self.nome:
            return '%s (%s)' % (self.nome, self.apelido)
        return self.nome or self.apelido
