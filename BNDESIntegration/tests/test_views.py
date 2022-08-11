from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.test import TestCase
from BNDESIntegration.models import Operacoes

class TestViews(TestCase):

    def test_request_get_take_database_valuew(self):
        try:
            Operacoes.objects.filter(cnpj=50746577000115)
            return HttpResponseRedirect(reverse('polls:cnpj', args=[50746577000115]))
        except Operacoes.DoesNotExist:
            return HttpResponseRedirect(reverse('buscar', args=[50746577000115]))


