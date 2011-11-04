#-*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from pagamentos.models import Lancamento

class NotificacaoMoipTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_existe_url_para_notificacao_moip(self):
        """
        Está definida uma URL para receber as notificações
        do MoIP
        """
        response = self._envia_notificacao_moip()
        self.assertNotEqual(response.status_code, 404)

    def test_notificao_somente_POST(self):
        """
        Somente o método POST pode ser utilizado para o
        recebimento de notificações
        """
        response = self._envia_notificacao_moip(method='GET')
        self.assertEqual(response.status_code, 405)

        response = self._envia_notificacao_moip()
        self.assertEqual(response.status_code, 200)

    def test_campos_obrigatorios_na_notificacao(self):
        response = self._envia_notificacao_moip(data={})
        self.assertEqual(response.status_code, 400)

    def test_armazena_doacao_a_partir_de_notificacao(self):
        self.assertTrue(len(Lancamento.objects.all()) == 0)
        response = self._envia_notificacao_moip()
        self.assertTrue(len(Lancamento.objects.all()) == 1)

    def _envia_notificacao_moip(self, **extra):
        if 'method' in extra:
            if extra['method'] == 'GET':
                return self.client.get(reverse('notificacao-moip'))

        if 'data' in extra:
            data = extra['data']
        else:
            data = {}
            required_fields = ['id_transacao', 'valor', 'status_pagamento', 'cod_moip', 'forma_pagamento', 'tipo_pagamento', 'email_consumidor']
            for field in required_fields:
                data[field] = ''

        data['valor'] = 1337.00

        return self.client.post(reverse('notificacao-moip'), data)

