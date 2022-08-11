from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone

import pytz


# Create your models here.

class Empresa(models.Model):
    """MODEL to store all requisited client doc
    """
    cnpj_id = models.BigIntegerField(primary_key=True)
    data_search = models.DateTimeField(
        default=datetime.now(pytz.timezone('America/Sao_Paulo')))
    validity_day = models.DateTimeField(
        default=(
            datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=30)))

    def __str__(self):
        return str(self.cnpj_id)

    def format_value(self):
        cnpj = str(self.cnpj_id)
        return '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])

    class Meta:
        db_table = 'tb_empresa_cnpj'
        verbose_name = 'BNDES.Empresa'


class Operacoes(models.Model):

    cnpj = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    agente_financeiro = models.CharField(max_length=100, default='null')
    operacaoDireta = models.CharField(default='null', max_length=10)
    inovacao = models.CharField(default='null', max_length=10)
    subsetorApoiado = models.CharField(max_length=100, default='null')
    reembolsavel = models.CharField(default='null', max_length=10)
    uf = models.CharField(max_length=100, default='null')
    produtoBndes = models.CharField(max_length=100, default='null')
    dataContratacao = models.CharField(max_length=100, default='null')
    liquidada = models.CharField(default='null', max_length=10)
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
    instrumentoBndes = models.CharField(
        max_length=100, null=True, default='null')
    naturezaCliente = models.CharField(
        max_length=100, null=True, default='null')
    prazoCarencia = models.CharField(max_length=100, null=True, default='null')
    tipoOperacao = models.CharField(max_length=100, null=True, default='null')
    cliente = models.CharField(max_length=100, null=True, default='null')
    tipoDocumento = models.CharField(max_length=100, null=True, default='null')
    fonteRecursos = models.CharField(max_length=100, null=True, default='null')
    cnpjAgenteFinanceiro = models.CharField(
        max_length=100, null=True, default='null')
    taxaJuros = models.SmallIntegerField(default=0)
    areaOperacional = models.CharField(
        max_length=200, null=True, default='null')
    codigoMunicipio = models.CharField(
        max_length=100, null=True, default='null')
    ramoAtividade = models.CharField(
        max_length=200, null=True, blank=True, default='null')

    def __str__(self):
        return 'cliente:' + self.cliente

    class Meta:
        verbose_name = 'operacoe'
        db_table = 'tb_bndes_operacao'


class BNDESOperacoes(models.Model):
    """MODEL to store BNDES operation requisited
    """
    client = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    logs = models.JSONField()
    data_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """MODEL class string

        returns:
            str : short description of model
        """
        return f'{self.client}'

    class Meta:
        db_table = 'tb_bndes_operacao_json'
        verbose_name = "BNDES.json.operacoe"
        ordering = ('data_created',)


class ArchiveBNDESOperacoes(models.Model):

    client = models.IntegerField()
    logs = models.JSONField()
    delete_data = models.DateField(default=datetime.today())

    def __str__(self):
        return f'{self.delete_data}'

    class Meta:
        db_table = 'tb_archive_bndes_operacao'
        verbose_name = 'BNDES.Archive'
        ordering = ('delete_data',)
