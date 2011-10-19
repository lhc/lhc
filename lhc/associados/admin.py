#-*- coding: utf-8 -*-
from django.contrib import admin
from associados.models import Associado

class AssociadoAdmin(admin.ModelAdmin):
  list_filter = ['em_atraso', 'ativo']
  list_display = ['nome', 'valor_mensalidade', 'ativo', 'em_atraso']

admin.site.register(Associado, AssociadoAdmin)
