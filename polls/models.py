
from time import time
from typing_extensions import Self
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models.signals import pre_save
import datetime
import pytz



# Create your models here.

class Empresa(models.Model):
    cnpj_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.cnpj_id)

    def format_value(self):
        cnpj = str(self.cnpj_id)
        return '{}.{}.{}/{}-{}'.format(cnpj[:2],cnpj[2:5],cnpj[5:8],cnpj[8:12],cnpj[12:])

class Operacoes(models.Model):

    cnpj = models.ForeignKey(Empresa,on_delete=models.CASCADE)
    agente_financeiro = models.CharField(max_length=100, default='null')
    operacaoDireta = models.BooleanField()
    inovacao = models.BooleanField()
    subsetorApoiado = models.CharField(max_length=100,default='null')
    reembolsavel = models.BooleanField()
    uf = models.CharField(max_length=100, default='null')
    produtoBndes = models.CharField(max_length=100, default='null')
    dataContratacao = models.CharField(max_length=100, default='null')
    liquidada = models.BooleanField()
    setorApoiado = models.CharField(max_length=100, default='null')
    custoFinanceiro = models.CharField(max_length=100, default='null')
    cnae = models.CharField(max_length=100, default='null')
    formaApoio = models.CharField(max_length=100, default='null')
    ano = models.IntegerField(default=0)
    valorDesembolsado = models.FloatField(null=True, default=0.0)
    porteCliente = models.CharField(max_length=100, null=True, default='null')
    municipio = models.CharField(max_length=100, null=True, default='null')
    prazoAmortizacao = models.IntegerField(default=0)
    cnpjAberto = models.CharField(max_length=100, null=True, default='null')
    instrumentoBndes = models.CharField(max_length=100, null=True, default='null')
    naturezaCliente = models.CharField(max_length=100, null=True, default='null')
    prazoCarencia = models.CharField(max_length=100, null=True, default='null')
    tipoOperacao = models.CharField(max_length=100, null=True, default='null')
    cliente = models.CharField(max_length=100, null=True, default='null')
    tipoDocumento = models.CharField(max_length=100, null=True, default='null')
    fonteRecursos = models.CharField(max_length=100, null=True, default='null')
    cnpjAgenteFinanceiro = models.CharField(max_length=100, null=True, default='null')
    taxaJuros = models.SmallIntegerField(default=0)
    areaOperacional = models.CharField(max_length=200, null=True, default='null')
    codigoMunicipio = models.CharField(max_length=100, null=True, default='null')
    ramoAtividade = models.CharField(max_length=200, null=True, blank=True, default='null')
    update_time = models.DateTimeField(default=datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))



    def __str__(self):
        return 'cliente:'  + self.cliente






