#-*- coding: utf-8 -*-
from django.test import TestCase

from associados.models import Associado
from pagamentos.models import Lancamento

import datetime

class LancamentoTestCase(TestCase):
# - Doação em um valor diferente da mensalidade de um associado valor maior
# - Doação em um valor diferente da mensalidade de um associado valor menor
# - Doação de um não associado

    def setUp(self):
        self.associado = Associado(nome='Associado Teste',
                                   email='associado@lhc.net.br',
                                   valor_mensalidade=1337.00)
        self.associado.save()
        Lancamento.objects.all().delete()

    def test_pagamento_mensalidade_associado(self):
        dados = {
            'data': datetime.date(2011, 11, 4),
            'valor': 1337.00,
            'origem': 'PAGSEG',
        }
        lancamento = Lancamento(**dados)
        lancamento.save(email_pagador=self.associado.email)

        self.assertEqual('MENSAL', lancamento.finalidade)
        self.assertEqual('Mensalidade de Novembro do associado Associado Teste', lancamento.descricao)
        self.assertEqual(1, len(Lancamento.objects.all()))

    def test_pagamento_de_nao_associado(self):
        dados = {
            'data': datetime.date(2011, 11, 4),
            'valor': 1337.00,
            'origem': 'PAGSEG',
        }
        lancamento = Lancamento(**dados)
        lancamento.save(email_pagador='naoassociado@email.com')

        self.assertEqual('DOACAO', lancamento.finalidade)
        self.assertEqual(u'Doação Anônima', lancamento.descricao)
        self.assertEqual(1, len(Lancamento.objects.all()))


