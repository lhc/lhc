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


class Doacao(models.Model):
  class Meta:
    verbose_name_plural = 'Doações'
    verbose_name = 'doação'

  def __unicode__(self):
    if self.membro:
      return '%s %s (R$ %s)' % (self.origem, self.membro, self.valor)
    return '%s (R$ %s)' % (self.origem, self.valor)


  ORIGEM = (
    ('MOIP', 'MoIP'),
    ('PAGS', 'PagSeguro'),
    ('CAIX', 'Caixa de Doação'),
    ('TEF ', 'Transferência Bancária'),
    ('BITC', 'BitCoin'),
  )
  MESES = (
    ('JAN', 'Janeiro'),
    ('FEV', 'Fevereiro'),
    ('MAR', 'Março'),
    ('ABR', 'Abril'),
    ('MAI', 'Maio'),
    ('JUN', 'Junho'),
    ('JUL', 'Julho'),
    ('AGO', 'Agosto'),
    ('SET', 'Setembro'),
    ('OUT', 'Outubro'),
    ('NOV', 'Novembro'),
    ('DEZ', 'Dezembro')
  )
  TIPOS = (
    ('MENS', 'Mensalidade'),
    ('ESPO', 'Espontânea'),
    ('BUFA', 'Buffer de Aluguel'),
  )

  valor = models.DecimalField(decimal_places=4, max_digits=10)
  data = models.DateField()

  origem = models.CharField(max_length=4, choices=ORIGEM)
  referencia = models.CharField(max_length=256, blank=True, null=True)
  tipo = models.CharField(max_length=4, choices=TIPOS)

  membro = models.ForeignKey(Associado, blank=True, null=True)

class Despesa(models.Model):
  def __unicode__(self):
    if self.descricao:
      return '%s (%s) (R$ %s)' % (self.tipo, self.descricao, self.valor)
    return '%s (R$ %s)' % (self.tipo, self.valor)

  TIPOS = (
    ('ALUG', 'Aluguel'),
    ('EQIP', 'Equipamento'),
    ('INFR', 'Infra-estrutura'),
    ('PRTY', 'Festa'),
    ('MISC', 'Miscelânea')
  )
  tipo = models.CharField(max_length=4, choices=TIPOS)
  descricao = models.CharField(max_length=1024, blank=True)
  valor = models.DecimalField(decimal_places=4, max_digits=10)
  responsavel = models.ForeignKey(Associado)
  data = models.DateField()
