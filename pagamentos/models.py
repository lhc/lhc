#-*- coding: utf-8 -*-
from django.db import models
from associados.models import Associado

TIPO_LANCAMENTO = (
    ('R', u'Receita'),
    ('D', u'Despesa'),
)

ORIGEM = (
    ('PAGSEGURO', u'PagSeguro'),
    ('MOIP', u'MoIP'),
    ('DOACAO', u'Caixa de Doação'),
)

FINALIDADE = (
    (u'Receita', (
            ('MENSAL', u'Mensalidade'),
            ('DOACAO', u'Doação Espontânea'),
        )
    ),
    (u'Despesa', (
            ('ALUGUEL', u'Aluguel'),
            ('INFRA', u'Infra-Estrutura'),
            ('EQUIPAMENT', u'Equipamentos'),
            ('REEMBOLSO', u'Reembolso'),
        )
    ),
)

MESES = ['', 'Janeiro', 'Fevereiro', u'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

class Lancamento(models.Model):
    data = models.DateField(verbose_name=u'Data')
    tipo = models.CharField(max_length=1, verbose_name=u'Tipo', choices=TIPO_LANCAMENTO)
    descricao = models.CharField(max_length=100, verbose_name=u'Descrição')
    valor = models.DecimalField(decimal_places=2, max_digits=20, verbose_name=u'Valor')
    origem = models.CharField(max_length=10, verbose_name=u'Origem', choices=ORIGEM)
    finalidade = models.CharField(max_length=10, verbose_name=u'Finalidade', choices=FINALIDADE)
    referencia = models.CharField(max_length=100, verbose_name=u'Referência', blank=True, null=True)
    associado = models.ForeignKey(Associado, verbose_name=u'Associado', blank=True, null=True)

    def __unicode__(self):
        return '[%s - R$ %s] %s' % (self.data, self.valor, self.descricao)

    def save(self, email_pagador=None, *args, **kwargs):
        if email_pagador is not None:
            try:
                self.associado = Associado.objects.get(email=email_pagador)
                if self.valor == self.associado.valor_mensalidade:
                    self.finalidade = 'MENSAL'
                    self.descricao = 'Mensalidade de %s do associado %s' % (MESES[self.data.month], self.associado.nome,)
            except Associado.DoesNotExist:
                self.finalidade = 'DOACAO'
                self.descricao = u'Doação Anônima'

        super(Lancamento, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'lançamento'
        verbose_name_plural = u'lançamentos'

