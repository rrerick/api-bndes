from django.shortcuts import render
from django.http import HttpResponse
from django.test import TestCase
import json
import requests
import pytz
from django.utils import timezone
import django.core.exceptions as expt
from BNDESIntegration.models import Operacoes, Empresa


class TestModel(TestCase):
    pass