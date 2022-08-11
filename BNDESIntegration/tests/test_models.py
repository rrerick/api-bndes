from django.shortcuts import render
from django.http import HttpResponse
from django.test import TestCase
import json,requests
import pytz
from django.utils import timezone
import django.core.exceptions as expt
from BNDESIntegration.models import Operacoes,Empresa



class TestModel(TestCase):

    def setUp (self):
        url="https://apis-gateway.bndes.gov.br/transparencia/v2/cliente/50746577000115"
        response = requests.get(url)

        data=response.json()
        self.empresas = Empresa(
            cnpj_id = 50746577000115
        )
        self.empresas.save()

        self.operacoes= Operacoes(
            cnpj = self.empresas,
            agente_financeiro = data['operacoes'][0]['agenteFinanceiro'],
            operacaoDireta = data['operacoes'][0]['operacaoDireta'],
            inovacao = data['operacoes'][0]['inovacao'],
            subsetorApoiado = data['operacoes'][0]['subsetorApoiado'],
            reembolsavel = data['operacoes'][0]['reembolsavel'],
            uf = data['operacoes'][0]['uf'],
            produtoBndes = data['operacoes'][0]['produtoBndes'],
            dataContratacao = data['operacoes'][0]['dataContratacao'],
            liquidada = data['operacoes'][0]['liquidada'],
            setorApoiado = data['operacoes'][0]['setorApoiado'],
            custoFinanceiro = data['operacoes'][0]['custoFinanceiro'],
            cnae = data['operacoes'][0]['cnae'],
            formaApoio = data['operacoes'][0]['formaApoio'],
            ano = data['operacoes'][0]['ano'],
            valorDesembolsado = data['operacoes'][0]['valorDesembolsado'],
            porteCliente = data['operacoes'][0]['porteCliente'],
            municipio = data['operacoes'][0]['municipio'],
            prazoAmortizacao = data['operacoes'][0]['prazoAmortizacao'],
            cnpjAberto = data['operacoes'][0]['cnpjAberto'],
            instrumentoBndes = data['operacoes'][0]['instrumentoBndes'],
            naturezaCliente = data['operacoes'][0]['naturezaCliente'],
            prazoCarencia = data['operacoes'][0]['prazoCarencia'],
            tipoOperacao =  data['operacoes'][0]['tipoOperacao'],
            cliente = data['operacoes'][0]['cliente'],
            tipoDocumento = data['operacoes'][0]['tipoDocumento'],
            fonteRecursos = data['operacoes'][0]['fonteRecursos'],
            cnpjAgenteFinanceiro = data['operacoes'][0]['cnpjAgenteFinanceiro'],
            taxaJuros = data['operacoes'][0]['taxaJuros'],
            areaOperacional = data['operacoes'][0]['areaOperacional'],
            codigoMunicipio = data['operacoes'][0]['codigoMunicipio'],
            ramoAtividade = data['operacoes'][0]['ramoAtividade'],

        )
        self.operacoes.save()
        self.objeto1 = Operacoes.objects.all().count()

    def test_have_value_in_update_time(self):
        print(self.operacoes.update_time)

