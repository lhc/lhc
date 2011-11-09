#-*- coding: utf-8 -*-
from django.contrib import admin
from pagamentos.models import Lancamento

class LancamentoAdmin(admin.ModelAdmin):
    list_filter = ['data', 'origem', 'tipo', 'associado', 'finalidade']
    list_display = ['data', 'origem', 'descricao', 'valor', 'tipo', 'finalidade', 'associado']
    fieldsets = [
      ('Informações', {'fields': ['data', 'valor', 'descricao', 'associado', 'tipo', 'finalidade']}),
      ('Origem', 		{'fields': ['origem', 'referencia',]}),
    ]

admin.site.register(Lancamento, LancamentoAdmin)
