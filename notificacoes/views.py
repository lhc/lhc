#-*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST

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

    return HttpResponse()

def _obter_dados_transacao(codigo_notificacao):
    try:
        TOKEN_PAGSEGURO = settings.TOKEN_PAGSEGURO
        EMAIL_PAGSEGURO = settings.EMAIL_PAGSEGURO
        URL_CONSULTA = settings.URL_CONSULTA_NOTIFICACAO_PAGSEGURO

#        xml_transacao = urllib2.urlopen(url_consulta % (transacao, settings.EMAIL_PAGSEGURO, settings.TOKEN_PAGSEGURO)).read()

        return {}
    except AttributeError:
        return {'erro': 'settings incompleto'}
