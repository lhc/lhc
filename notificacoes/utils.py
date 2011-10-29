#-*- coding: utf-8 -*-
from django.conf import settings

import time
import urllib2
import xml.dom.minidom as minidom

def _get_value_from_dom(root, tag):
    return root[0].getElementsByTagName(tag)[0].childNodes[0].data

def obter_dados_transacao_pagseguro(codigo_notificacao):
    '''
    A partir de uma notificação de mudança de status de uma transação,
    obter os dados completos dela a partir do webservice do pagseguro
    '''
    pass
    dados_transacao = {}
    try:
        TOKEN_PAGSEGURO = settings.TOKEN_PAGSEGURO
        EMAIL_PAGSEGURO = settings.EMAIL_PAGSEGURO
        URL_CONSULTA = settings.URL_CONSULTA_NOTIFICACAO_PAGSEGURO

        xml_transacao = urllib2.urlopen(URL_CONSULTA % (codigo_notificacao, EMAIL_PAGSEGURO, TOKEN_PAGSEGURO)).read()

        doc = minidom.parseString(xml_transacao)
        node = doc.documentElement
        transaction = doc.getElementsByTagName("transaction")

        data = _get_value_from_dom(transaction, "date")
        data = data.split("T")[0]
        data = time.strptime(data, '%Y-%m-%d')
        data = time.strftime('%Y-%m-%d', data)
        dados_transacao["date"] = data
        dados_transacao["code"] = _get_value_from_dom(transaction, "code")
        dados_transacao["status"] = _get_value_from_dom(transaction, "status")
        dados_transacao["grossAmount"] = _get_value_from_dom(transaction, "grossAmount")
        dados_transacao["feeAmount"] = _get_value_from_dom(transaction, "feeAmount")

        sender = transaction[0].getElementsByTagName("sender")
        dados_transacao['sender_email'] = _get_value_from_dom(sender, "email")
        dados_transacao['sender_name'] = _get_value_from_dom(sender, "name")

    except AttributeError:
        dados_transacao['erro'] = 'settings incompleto'

    return dados_transacao
