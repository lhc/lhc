#-*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from notificacoes.utils import obter_dados_transacao_pagseguro

import urllib2

class NotificacaoPagseguroTestCase(TestCase):
    '''
    - Resolver duplicação do host permitido entre o teste e o código
    '''

    def setUp(self):
        self.client = Client()

    def test_existe_url_para_notificacao_pagseguro(self):
        """
        Está definida uma URL para receber as notificações
        do PagSeguro
        """
        response = self._envia_notificacao('GET')
        self.assertNotEqual(response.status_code, 404)

    def test_notificao_somente_POST(self):
        """
        Somente o método POST pode ser utilizado para o
        recebimento de notificações
        """
        response = self._envia_notificacao(method='GET')
        self.assertEqual(response.status_code, 405)

        response = self._envia_notificacao()
        self.assertEqual(response.status_code, 200)

    def test_campos_obrigatorios_na_notificacao(self):
        response = self._envia_notificacao(data={})
        self.assertEqual(response.status_code, 400)

    def test_notificacoes_somente_pagseguro_host(self):
        response = self._envia_notificacao(HTTP_HOST = 'host.sem.permissao.com')
        self.assertEqual(response.status_code, 403)
        response = self._envia_notificacao(HTTP_HOST = 'pagseguro.uol.com.br')
        self.assertEqual(response.status_code, 200)

    def _envia_notificacao(self, method='POST', data={'notificationCode':'', 'notificationType':''}, **extra):

        if 'HTTP_HOST' not in extra:
            extra['HTTP_HOST'] = 'pagseguro.uol.com.br'

        if method == 'POST':
            return self.client.post(reverse('notificacao-pagseguro'), data, **extra)
        return self.client.get(reverse('notificacao-pagseguro'))

class ObtencaoDadosTransacaoTestCase(TestCase):

    def setUp(self):
        settings.TOKEN_PAGSEGURO = 'AD6D463C6G2F42259B17A6443056C0FA'
        settings.EMAIL_PAGSEGURO = 'usuario@pagseguro.com.br'
        settings.URL_CONSULTA_NOTIFICACAO_PAGSEGURO = 'http://fakeurl.com%s%s%s'
        self.codigo_notificacao = '766B9C-AD4B044B04DA-77742F5FA653-E1AB24'

    def test_settings_obrigatorios(self):
        dados_transacao = obter_dados_transacao_pagseguro(self.codigo_notificacao)
        self.assertTrue('erro' not in dados_transacao)

    def test_token_obrigatorio(self):
        del settings.TOKEN_PAGSEGURO
        dados_transacao = obter_dados_transacao_pagseguro(self.codigo_notificacao)
        self.assertTrue('erro' in dados_transacao)

    def test_email_obrigatorio(self):
        del settings.EMAIL_PAGSEGURO
        dados_transacao = obter_dados_transacao_pagseguro(self.codigo_notificacao)
        self.assertTrue('erro' in dados_transacao)

    def test_url_consulta_notificacao_obrigatorio(self):
        del settings.URL_CONSULTA_NOTIFICACAO_PAGSEGURO
        dados_transacao = obter_dados_transacao_pagseguro(self.codigo_notificacao)
        self.assertTrue('erro' in dados_transacao)

    def test_obter_dados_do_xml(self):
        import notificacoes.utils
        notificacoes.utils.urllib2.urlopen = fake_urllib2
        dados = obter_dados_transacao_pagseguro(self.codigo_notificacao, )
        self.assertEqual("2011-02-10", dados['date'])
        self.assertEqual('9E884542-81B3-4419-9A75-BCC6FB495EF1', dados['code'])
        self.assertEqual('3', dados['status'])
        self.assertEqual('49900.00', dados['grossAmount'])
        self.assertEqual('0.00', dados['feeAmount'])
        self.assertEqual('comprador@uol.com.br', dados['sender_email'])
        self.assertEqual('Comprador', dados['sender_name'])

    def tearDown(self):
        try:
            del settings.TOKEN_PAGSEGURO
        except AttributeError:
            pass

        try:
            del settings.EMAIL_PAGSEGURO
        except AttributeError:
            pass

        try:
            del settings.URL_CONSULTA_NOTIFICACAO_PAGSEGURO
        except AttributeError:
            pass

def fake_urllib2(*args, **extra):
    class dummy:
        def read(self):
            return '''<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>  
<transaction>  
    <date>2011-02-10T16:13:41.000-03:00</date>  
    <code>9E884542-81B3-4419-9A75-BCC6FB495EF1</code>  
    <reference>REF1234</reference>  
    <type>1</type>  
    <status>3</status>  
    <paymentMethod>  
        <type>1</type>  
        <code>101</code>  
    </paymentMethod>  
    <grossAmount>49900.00</grossAmount>  
    <discountAmount>0.00</discountAmount>  
    <feeAmount>0.00</feeAmount>  
    <netAmount>49900.00</netAmount>  
    <extraAmount>0.00</extraAmount>  
    <installmentCount>1</installmentCount>  
    <itemCount>2</itemCount>  
    <items>  
        <item>  
            <id>0001</id>  
            <description>Notebook Prata</description>  
            <quantity>1</quantity>  
            <amount>24300.00</amount>  
        </item>  
        <item>  
            <id>0002</id>  
            <description>Notebook Rosa</description>  
            <quantity>1</quantity>  
            <amount>25600.00</amount>  
        </item>  
    </items>  
    <sender>  
        <name>Comprador</name>  
        <email>comprador@uol.com.br</email>  
        <phone>  
            <areaCode>11</areaCode>  
            <number>56273440</number>  
        </phone>  
    </sender>  
    <shipping>  
        <address>  
            <street>Av. Brig. Faria Lima</street>  
            <number>1384</number>  
            <complement>5o andar</complement>  
            <district>Jardim Paulistano</district>  
            <postalCode>01452002</postalCode>  
            <city>Sao Paulo</city>  
            <state>SP</state>  
            <country>BRA</country>  
        </address>  
        <type>1</type>  
        <cost>21.50</cost>  
    </shipping>  
</transaction>  '''
    return dummy()
