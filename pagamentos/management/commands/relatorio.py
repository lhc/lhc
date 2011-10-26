# -*- coding: utf-8 -*-

# FIXME
#     - Balanco anterior
#     - Marcar membros atrasados como tal?
#     - Pagaram *este* mes, para o *proximo*
#     - Pagaram mes *anterior* para *este mes*
#     - Atualmente considera qualquer doacao como mensalidade, ignora tipo==MENS
#

import datetime
from decimal import Decimal
from collections import defaultdict
from django.core.management.base import BaseCommand, CommandError
from doacoes.models import Membro, Doacao, Despesa

ALUGUEL = 600
BUFFER = 3 * ALUGUEL

TRADUZ = {
  'mensalidade': 'Mensalidades',
  'membro': u'Doações de membro',
  'anonima': u'Doações anônimas',
  'ALUG': 'Aluguel',
  'EQIP': 'Equipamento',
  'INFR': 'Infra-estrutura',
  'PRTY': 'Festa',
  'MISC': u'Miscelânea',
  'MENS': 'Mensalidade',
  'ESPO': u'Espontânea',
  'BUFA': 'Buffer de Aluguel'
}

def print_titulo(titulo, separador='-'):
  print titulo
  print separador * len(titulo)

def format_nome(nome):
  splitted = nome.split()
  return splitted[0] + ' ' + splitted[-1]

def format_string(max_length):
  return '%%-%ds' % (max_length + 2)

def format_descricao(descricao, max_length):
  if len(descricao) < max_length:
    return descricao
  return '%s...' % descricao[-(max_length-3):]

def print_item_doacao(doacao, max_length):
  FORMAT_STRING = format_string(max_length)
  if doacao.membro:
    print '%s    %s %10.2f' % (doacao.data, FORMAT_STRING % format_nome(doacao.membro.nome), Decimal(doacao.valor)),
  elif doacao.origem == 'CAIX' and doacao.referencia:
    print '%s    %s %10.2f' % (doacao.data, FORMAT_STRING % format_descricao(doacao.referencia, max_length), Decimal(doacao.valor)),
  else:
    print '%s    %s %10.2f' % (doacao.data, FORMAT_STRING % 'Anonima', Decimal(doacao.valor)),
  print '(%s)' % doacao.origem

def print_item_despesa(despesa, max_length):
  FORMAT_STRING = format_string(max_length)
  if despesa.descricao:
    print '%s    %s %10.2f' % (despesa.data, FORMAT_STRING % format_descricao(despesa.descricao, max_length), Decimal(despesa.valor))
  elif despesa.responsavel:
    print '%s    %s %10.2f' % (despesa.data, FORMAT_STRING % TRADUZ[despesa.tipo], Decimal(despesa.valor))
  else:
    print '%s    %s %10.2f' % (despesa.data, FORMAT_STRING % TRADUZ[despesa.tipo], Decimal(despesa.valor))

def print_agrupado(grupos, max_length):
  FORMAT_STRING = format_string(max_length)
  total = Decimal(0)
  for grupo, itens in grupos.items():
    print_titulo(TRADUZ[grupo])
    
    total_grupo = Decimal(0)
    
    for item in itens:
      total_grupo = total_grupo + Decimal(item.valor)

      if isinstance(item, Doacao):
        print_item_doacao(item, max_length)
      elif isinstance(item, Despesa):
        print_item_despesa(item, max_length)

    total += total_grupo
    print '              %s %10.2f           %10.2f' % (FORMAT_STRING % 'TOTAL PARCIAL', total_grupo, total)
  
  print '              %s                      %s' % (FORMAT_STRING % '', '-' * 10)
  print '              %s                      %10.2f' % (FORMAT_STRING % 'TOTAL', total)
  
def processa_entrada():
  total = Decimal(0)
  total_buffer = Decimal(0)
  print_titulo('ENTRADA', '=')

  max_length = 0
  doacoes_agrupado = defaultdict(lambda *ignore: [])
  for doacao in Doacao.objects.all().order_by('data'):
    total = total + Decimal(doacao.valor)

    if doacao.tipo == 'BUFA':
      total_buffer = total_buffer + Decimal(doacao.valor)

    if doacao.tipo == 'MENS':
      doacoes_agrupado['mensalidade'].append(doacao)
    elif doacao.membro:
      if len(doacao.membro.nome) > max_length:
        max_length = len(doacao.membro.nome)

      doacoes_agrupado['membro'].append(doacao)
    else:
      doacoes_agrupado['anonima'].append(doacao)

  print_agrupado(doacoes_agrupado, max_length)

  return total, total_buffer, max_length

def processa_saida(max_length):
  total = Decimal(0)
  print_titulo(u'SAÍDA', '=')
  
  saida_agrupado = defaultdict(lambda *ignore: [])
  for despesa in Despesa.objects.all().order_by('data'):
    total = total + Decimal(despesa.valor)
    saida_agrupado[despesa.tipo].append(despesa)
  
  print_agrupado(saida_agrupado, max_length)
  
  return total
    
def processa_balanco(total_entrada, total_saida, total_buffer, max_length):
  FORMAT_STRING = format_string(max_length)
  print_titulo(u'BALANÇO', '=')
  
  print '              %s  %10.2f' % (FORMAT_STRING % 'Total entrada', total_entrada)
  print '              %s -%10.2f' % (FORMAT_STRING % u'Total saída', total_saida)
  print '              %s -%10.2f' % (FORMAT_STRING % 'Buffer de aluguel', total_buffer)
  print '              %s  %s'     % (FORMAT_STRING % '', '-' * 10)
  
  balanco = total_entrada - total_saida - total_buffer
  print '              %s  %10.2f' % (FORMAT_STRING % u'Balanço parcial', balanco)
  
  if Decimal(total_buffer) < Decimal(BUFFER):
    ajuste = Decimal(600 * 3) - Decimal(total_buffer)
    print '              %s -%10.2f' % (FORMAT_STRING % u'Ajuste buffer', ajuste)
    balanco -= ajuste
  else:
    print '              %s  %10.2f' % (FORMAT_STRING % u'Ajuste buffer', 0)
    
  print '              %s  %s'     % (FORMAT_STRING % '', '-' * 10)
  print '              %s  %10.2f' % (FORMAT_STRING % u'Balanço final', balanco)

def seu_madruga():
  print_titulo(u'INADIMPLÊNCIA', '=')
  
  today = datetime.datetime.today()
  last_month = today - datetime.timedelta(days=30)

  pagantes = set(doacao.membro for doacao in Doacao.objects.filter(data__gt=last_month, data__lt=today, membro__isnull=False))
  inadimplentes = set(membro for membro in Membro.objects.filter(ativo=True, em_atraso=False) if not membro in pagantes)
  
  two_months_ago = last_month - datetime.timedelta(days=30)
  atrasados = set(doacao.membro
        for doacao in
          Doacao.objects.filter(data__lt=last_month, data__gt=two_months_ago, membro__isnull=False)
            if not doacao.membro in pagantes or
              doacao.membro in inadimplentes or
              doacao.membro.em_atraso)
  
  if pagantes:
    print u'Pagaram para este mês'
    print '---------------------'
    for pagante in pagantes:
      print format_nome(pagante.nome)
  else:
    print u'*** NINGUÉM PAGOU PARA ESTE MES ***'
  
  if inadimplentes:
    print u'\nNão pagaram para este mês'
    print '--------------------'
    for inadimplente in inadimplentes:
      print format_nome(inadimplente.nome)
  else:
    print u'*** TODO MUNDO PAGOU ESSE MES ***'
  
  if atrasados:
    print u'\nEm atraso'
    print '---------'
    for antigo in atrasados:
      print format_nome(antigo.nome)
  else:
    print u'*** NINGUÉM EM ATRASO ***'  

class Command(BaseCommand):
  args = None
  help = 'Generates a report'
  
  def handle(self, *args, **options):
    total_entrada, total_buffer, max_length = processa_entrada()
    total_saida = processa_saida(max_length)
    processa_balanco(total_entrada, total_saida, total_buffer, max_length)
    
    seu_madruga()
