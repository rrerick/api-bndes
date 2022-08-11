from django.contrib import admin
from .models import Transaction, Company, BNDESTransaction, ArchiveBNDESTransaction

# Register your models here.
admin.site.register(
    [Transaction, Company, BNDESTransaction, ArchiveBNDESTransaction])
