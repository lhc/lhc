#-*- coding: utf-8 -*-
from django.contrib import admin
from pagamentos.models import Pagamento, Doacao, Despesa

admin.site.register(Pagamento)
admin.site.register(Despesa)
admin.site.register(Doacao)

class DoacaoAdmin(admin.ModelAdmin):
  list_filter = ['data', 'origem', 'tipo']
  list_display = ['origem', 'data', 'valor', 'membro', 'tipo']
  fieldsets = [
    (None,		{'fields': ['valor', 'data', 'membro', 'tipo']}),
    ('Origem', 		{'fields': ['origem', 'referencia']}),
  ]

class DespesaAdmin(admin.ModelAdmin):
  list_filter = ['data', 'tipo']
  list_display = ['data', 'tipo', 'descricao', 'responsavel', 'valor']

admin.site.register(Doacao, DoacaoAdmin)
admin.site.register(Despesa, DespesaAdmin)
