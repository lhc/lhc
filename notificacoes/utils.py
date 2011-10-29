#-*- coding: utf-8 -*-
from django.conf import settings

def obter_dados_transacao_pagseguro(codigo_notificacao):
    '''
    A partir de uma notificação de mudança de status de uma transação,
    obter os dados completos dela a partir do webservice do pagseguro
    '''
    try:
        TOKEN_PAGSEGURO = settings.TOKEN_PAGSEGURO
        EMAIL_PAGSEGURO = settings.EMAIL_PAGSEGURO
        URL_CONSULTA = settings.URL_CONSULTA_NOTIFICACAO_PAGSEGURO

#        xml_transacao = urllib2.urlopen(url_consulta % (transacao, settings.EMAIL_PAGSEGURO, settings.TOKEN_PAGSEGURO)).read()

        return {}
    except AttributeError:
        return {'erro': 'settings incompleto'}
