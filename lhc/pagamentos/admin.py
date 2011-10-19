#-*- coding: utf-8 -*-
from django.contrib import admin
from pagamentos.models import Pagamento, Doacao, Despesa

admin.site.register(Pagamento)
admin.site.register(Despesa)
admin.site.register(Doacao)
