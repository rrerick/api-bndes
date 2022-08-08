from django.contrib import admin
from .models import Operacoes, Empresa

# Register your models here.
admin.site.register([Operacoes,Empresa])