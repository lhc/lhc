#-*- coding: utf-8 -*-
from django.contrib import admin
from pagamentos.models import Lancamento

class LancamentoAdmin(admin.ModelAdmin):
  list_filter = ['data', 'origem', 'tipo']
  list_display = ['origem', 'data', 'valor', 'associado', 'tipo']
  fieldsets = [
    (None,		{'fields': ['valor', 'data', 'associado', 'tipo']}),
    ('Origem', 		{'fields': ['origem', 'referencia']}),
  ]

admin.site.register(Lancamento, LancamentoAdmin)
