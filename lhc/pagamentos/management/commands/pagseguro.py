#-*- coding: utf-8 -*-

import time
import sys
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from xml.dom.minidom import parse
from doacoes.models import Membro, Doacao

def val(root, tag):
  return root.getElementsByTagName(tag)[0].childNodes[0].data

def handle_table(root):
  referencia = val(root, 'Transacao_ID')
  email = val(root, 'Cliente_Email')
  status = val(root, 'Status')
  valor = val(root, 'Valor_Liquido').replace(',', '.')
  valor_bruto = val(root, 'Valor_Bruto').replace(',', '.')
  data = val(root, 'Data_Transacao')
  tipo = val(root, 'Tipo_Transacao')
  
  data = time.strptime(data, '%d/%m/%Y %H:%M:%S')
  data = time.strftime('%Y-%m-%d', data)
  
  try:
    membro = Membro.objects.get(email=email)
    mensalidade = Decimal(membro.valor_mensalidade) > 0 and Decimal(valor_bruto) >= Decimal(membro.valor_mensalidade)
    tipo = 'MENS' if mensalidade else 'ESPO'
  except Membro.DoesNotExist:
    membro = None
    tipo = 'ESPO'

  if tipo == 'MENS':
    print 'Mensalidade de %s paga (R$ %s)' % (membro, valor_bruto)
  elif membro:
    print 'Doacao do membro %s de R$ %s recebida' % (membro, valor_bruto)
  else:
    print 'Doacao anonima de R$ %s recebida' % valor_bruto

  doacao = Doacao(valor=valor, data=data, origem='PAGS', referencia=referencia, membro=membro, tipo=tipo)
  doacao.save()

def handle_new_data_set(root):
  for table in root.getElementsByTagName('Table'):
    handle_table(table)

class Command(BaseCommand):
  args = '<xml path>'
  help = 'Parses a PagSeguro XML and updates donation table'
  
  def handle(self, *args, **options):
    for path in args:
      print 'Parsing', path
      handle_new_data_set(parse(path))
