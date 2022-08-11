from django.template import Context
from django.urls import path, re_path
from sympy import linear_eq_to_matrix
from . import views


app_name = 'BNDESIntegration'
urlpatterns = [

    re_path(r"^(?P<nome>operacoes|desembolsos|all)/(?P<cnpj>\d{11,14})/$",
            views.BNDESDatasetGetView.as_view(), name='search'),


]
