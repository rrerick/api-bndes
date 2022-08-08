import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, FormView, DetailView
import requests
from polls import serializers
from polls.models import Operacoes, Empresa
from .forms import CnpjForm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import datetime
from django.core import serializers
# Create your views here.


class FormCnpjView(FormView):

    form_class = CnpjForm
    template_name = 'polls/form_cnpj.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return HttpResponseRedirect(reverse('polls:cnpj', args=[form.__str__('cnpj')]))


def SearchDataBase(request, cnpj):
    """
    Filter on cnpj requests
    if exists redirect to a validator, if not redirect to registration
    """
    try:
        Empresa.objects.get(cnpj_id=cnpj)
    except Empresa.DoesNotExist:
        return HttpResponseRedirect(reverse('polls:cnpj', args=[cnpj]))
    return HttpResponseRedirect(reverse('polls:validador', args=[cnpj]))


def view_expiration_date(request, cnpj):
    """
    Validate if the data expiry 
    expiration date == 1 mounth
    """
    operacoes_object = Operacoes.objects.filter(cnpj=cnpj).values()

    try:
        naive = operacoes_object[0]['update_time'] + \
            datetime.timedelta(days=30)
        if operacoes_object[0]['update_time'] < naive:
            # update_time é menor que 30 dias
            return HttpResponseRedirect(reverse('polls:informacao', args=[cnpj]))
        else:
            # update_time é maior que 30 dias, hora de deletar e pegar uma nova
            operacoes_object.delete()
            return HttpResponseRedirect(reverse('polls:buscar', args=cnpj))
    except IndexError:
        return HttpResponse('{}')


class ListDataView(ListView):
    """
    List all informations about a CNPJ
    """
    paginate_by = 15
    model = Operacoes
    template_name = 'polls/home2.html'
    context_object_name = 'nome'

    def get_queryset(self):
        return Operacoes.objects.filter(cnpj=self.kwargs['cnpj'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresas'] = Empresa.objects.get(cnpj_id=self.kwargs['cnpj'])
        return context


def FoundCnpj(request, cnpj):
    """
    Registration of CNPJ request into database.
    """
    tabela1 = Empresa(
        cnpj_id=cnpj
    )
    tabela1.save()
    return render(request, 'polls/home.html', {'nome': tabela1})


def busca_dados(request, cnpj):
    """
    Get info on BNDES API and insert into DATABASE
    """

    # request to BNDES API
    url = "https://apis-gateway.bndes.gov.br/transparencia/v2/cliente/%s" % (
        cnpj)

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(url)
    data = response.json()

    # campos variaveis entre null e com informação
    cnpjAgenteFinanceiro_list = []
    municipio_list = []
    agenteFinanceiro_list = []
    ramoAtividade_list = []
    custoFinanceiro_list = []
    taxaJuros_list = []
    prazoAmortizacao_list = []
    prazoCarencia_list = []
    lists_name = [ramoAtividade_list, custoFinanceiro_list, taxaJuros_list, prazoAmortizacao_list,
                  prazoCarencia_list, agenteFinanceiro_list, municipio_list, cnpjAgenteFinanceiro_list]
    values_list = ['ramoAtividade', 'custoFinanceiro', 'taxaJuros', 'prazoAmortizacao',
                   'prazoCarencia', 'agenteFinanceiro', 'municipio', 'cnpjAgenteFinanceiro']
    x = 0
    y = 0
    value = True
    while value == True:
        try:
            nome = lists_name[x]
            nome_campo = values_list[x]
        except IndexError:
            value = False

        try:
            if values_list[x] in data['operacoes'][y]:
                print('aqui', nome_campo)
                nome.append(data['operacoes'][y][nome_campo])
            else:
                print('nao aqui', nome_campo)
                nome.append(0)
            y += 1
        except IndexError:
            x += 1
            y = 0
            continue

    # Insert Into Operacoes
    for loop in range(200):
        try:

            operacoes, created = Operacoes.objects.filter(cnpj=cnpj).get_or_create(
                cnpj=Empresa.objects.get(cnpj_id=cnpj),
                agente_financeiro=agenteFinanceiro_list[loop],
                operacaoDireta=data['operacoes'][loop]['operacaoDireta'],
                inovacao=data['operacoes'][loop]['inovacao'],
                subsetorApoiado=data['operacoes'][loop]['subsetorApoiado'],
                reembolsavel=data['operacoes'][loop]['reembolsavel'],
                uf=data['operacoes'][loop]['uf'],
                produtoBndes=data['operacoes'][loop]['produtoBndes'],
                dataContratacao=data['operacoes'][loop]['dataContratacao'],
                liquidada=data['operacoes'][loop]['liquidada'],
                setorApoiado=data['operacoes'][loop]['setorApoiado'],
                custoFinanceiro=custoFinanceiro_list[loop],
                cnae=data['operacoes'][loop]['cnae'],
                formaApoio=data['operacoes'][loop]['formaApoio'],
                ano=data['operacoes'][loop]['ano'],
                valorDesembolsado=data['operacoes'][loop]['valorDesembolsado'],
                porteCliente=data['operacoes'][loop]['porteCliente'],
                municipio=municipio_list[loop],
                prazoAmortizacao=prazoAmortizacao_list[loop],
                cnpjAberto=data['operacoes'][loop]['cnpjAberto'],
                instrumentoBndes=data['operacoes'][loop]['instrumentoBndes'],
                naturezaCliente=data['operacoes'][loop]['naturezaCliente'],
                prazoCarencia=prazoCarencia_list[loop],
                tipoOperacao=data['operacoes'][loop]['tipoOperacao'],
                cliente=data['operacoes'][loop]['cliente'],
                tipoDocumento=data['operacoes'][loop]['tipoDocumento'],
                fonteRecursos=data['operacoes'][loop]['fonteRecursos'],
                cnpjAgenteFinanceiro=cnpjAgenteFinanceiro_list[loop],
                taxaJuros=taxaJuros_list[loop],
                areaOperacional=data['operacoes'][loop]['areaOperacional'],
                codigoMunicipio=data['operacoes'][loop]['codigoMunicipio'],
                ramoAtividade=ramoAtividade_list[loop],
            )
            operacoes.save()
        except Exception as e:
            print(e)
            break

    try:
        is_ok = Operacoes.objects.filter(cnpj=cnpj)

    except Operacoes.DoesNotExist:
        return HttpResponse('{}')

    return HttpResponseRedirect(reverse('polls:informacao', args=[cnpj]))


class DetailOperationView(DetailView):
    model = Operacoes
    template_name = 'polls/details.html'
    context_object_name = 'detail'
    pk_url_kwarg = 'pk'
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        response = serializers.serialize(
            "json",  Operacoes.objects.filter(pk=self.kwargs['pk']))
        dict = json.loads(response)
        return JsonResponse(dict, safe=False)
