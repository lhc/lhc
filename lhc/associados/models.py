#-*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Associado(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=12)

    def __unicode__(self):
        return self.nome
