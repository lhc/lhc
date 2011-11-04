#-*- coding: utf-8 -*
from django.conf import settings
from django.test import TestCase

from notificacoes.tests.helper import *
from notificacoes.utils import obter_dados_transacao_pagseguro


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
        notificacoes.utils.urllib2.urlopen = urllib2_pagseguro_mock
        dados = obter_dados_transacao_pagseguro(self.codigo_notificacao)

        dados_lancamento = dados['lancamento']
        dados_pagador = dados['pagador']

        self.assertEqual("2011-02-10", dados_lancamento['data'])
        self.assertEqual('9E884542-81B3-4419-9A75-BCC6FB495EF1', dados_lancamento['referencia'])
        self.assertEqual('49900.00', dados_lancamento['valor'])
        self.assertEqual('comprador@uol.com.br', dados_pagador['email'])

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
