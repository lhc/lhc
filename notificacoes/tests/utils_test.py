#-*- coding: utf-8 -*
from django.conf import settings
from django.test import TestCase

from notificacoes.tests.helper import *
from notificacoes.utils import obter_dados_transacao_pagseguro

#import urllib2

class ObtencaoDadosTransacaoPagseguroTestCase(TestCase):

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
