#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

# - duplicação do host permitido no teste e no codigo
# - configuração settings TOKEN e EMAIL
# - mock urllib2
# - obter xml

class NotificacaoPagseguroTestCase(TestCase):

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
