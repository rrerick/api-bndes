from django.contrib import admin
from .models import Operacoes, Empresa, BNDESOperacoes, ArchiveBNDESOperacoes

# Register your models here.
admin.site.register(
    [Operacoes, Empresa, BNDESOperacoes, ArchiveBNDESOperacoes])
