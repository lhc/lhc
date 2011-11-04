#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from notificacoes.utils import obter_dados_transacao_pagseguro
from pagamentos.models import Lancamento

@require_POST
def processa_pagseguro(request):
    '''
    Processa uma notificação de transação enviada pelo PagSeguro quando ocorrer
    alguma mudança no status de alguma transação.
    (referência: https://pagseguro.uol.com.br/v2/guia-de-integracao/api-de-notificacoes.html)
    '''
    if 'notificationCode' not in request.POST or 'notificationType' not in request.POST:
        return HttpResponse(status=400)

    allowed_hosts = ['pagseguro.uol.com.br',]
    if request.get_host() not in allowed_hosts:
        return HttpResponse(status=403)

    dados = obter_dados_transacao_pagseguro(request.POST['notificationCode'])
    lancamento = Lancamento(**dados['lancamento'])
    lancamento.save(email_pagador=dados['pagador']['email'])

    return HttpResponse()

@require_POST
def processa_moip(request):
    required_fields = ['id_transacao', 'valor', 'status_pagamento', 'cod_moip', 'forma_pagamento', 'tipo_pagamento', 'email_consumidor']
    for field in required_fields:
        if field not in request.POST:
            return HttpResponse(status=400)

    # TODO criar dicionário com os dados
    #armazenar_pagamento(dados)

    return HttpResponse()
