#-*- coding: utf-8 -*-
#!-*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^pagseguro', 'notificacoes.views.processa_pagseguro', name='notificacao-pagseguro'),

    url(r'^moip', 'notificacoes.views.processa_moip', name='notificacao-moip'),
)

