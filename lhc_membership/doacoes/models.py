# -*- coding: utf-8 -*-
from django.db import models

class Membro(models.Model):
  def __unicode__(self):
    if self.apelido and self.nome:
      return '%s (%s)' % (self.nome, self.apelido)
    if self.nome:
      return self.nome
    if self.apelido:
      return self.apelido
    if self.email:
      return self.email
    return 'Membro %d' % self.id
      

  nome = models.CharField(max_length=1024)
  apelido = models.CharField(max_length=256)
  email = models.CharField(max_length=256)
  telefone = models.CharField(max_length=32, null=True, blank=True)

  valor_mensalidade = models.DecimalField(decimal_places=4, max_digits=10)

  em_atraso = models.BooleanField(default=False)
  ativo = models.BooleanField(default=True)

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

  membro = models.ForeignKey(Membro, blank=True, null=True)

class Item(models.Model):
  class Meta:
    verbose_name_plural = 'Itens'

  TIPOS = (
    ('EQIP', 'Equipamento'),
    ('COMP', 'Componente'),
    ('MOVL', 'Móvel'),
    ('MISC', 'Miscelânea')
  )
  tipo = models.CharField(max_length=4, choices=TIPOS)
  nome = models.CharField(max_length=128)
  membro = models.ForeignKey(Membro, blank=True, null=True, related_name='item_dono')
  hackeavel = models.BooleanField(default=False)
  numero_serie = models.CharField(max_length=64)
  emprestado_para = models.ForeignKey(Membro, blank=True, null=True, related_name='item_emprestimo')
  funciona = models.BooleanField(default=True)

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
  responsavel = models.ForeignKey(Membro)
  data = models.DateField()
