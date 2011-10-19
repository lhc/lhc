from doacoes.models import Membro, Doacao, Despesa, Item
from django.contrib import admin

class MembroAdmin(admin.ModelAdmin):
  list_filter = ['em_atraso', 'ativo']
  list_display = ['nome', 'valor_mensalidade', 'ativo', 'em_atraso']

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

admin.site.register(Membro, MembroAdmin)
admin.site.register(Doacao, DoacaoAdmin)
admin.site.register(Despesa, DespesaAdmin)
admin.site.register(Item)