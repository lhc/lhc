#-*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from pagamentos.models import Doacao
from notificacoes.utils import obter_dados_transacao_pagseguro
from notificacoes.tests.helper import *

import urllib2

class NotificacaoPagseguroTestCase(TestCase):
    '''
    - Resolver duplicação do host permitido entre o teste e o código
    '''

    def setUp(self):
        self.client = Client()
        settings.TOKEN_PAGSEGURO = 'AD6D463C6G2F42259B17A6443056C0FA'
        settings.EMAIL_PAGSEGURO = 'usuario@pagseguro.com.br'
        settings.URL_CONSULTA_NOTIFICACAO_PAGSEGURO = 'http://fakeurl.com%s%s%s'
        self.codigo_notificacao = '766B9C-AD4B044B04DA-77742F5FA653-E1AB24'

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

    def test_armazena_doacao_a_partir_do_xml(self):
        import notificacoes.utils
        notificacoes.utils.urllib2.urlopen = fake_urllib2
        self.assertTrue(len(Doacao.objects.all()) == 0)
        response = self._envia_notificacao()
        self.assertTrue(len(Doacao.objects.all()) == 1)

    def _envia_notificacao(self, method='POST', data={'notificationCode':'', 'notificationType':''}, **extra):

        if 'HTTP_HOST' not in extra:
            extra['HTTP_HOST'] = 'pagseguro.uol.com.br'

        if method == 'POST':
            return self.client.post(reverse('notificacao-pagseguro'), data, **extra)
        return self.client.get(reverse('notificacao-pagseguro'))

