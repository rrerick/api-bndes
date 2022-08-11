from django.template import Context
from django.urls import path, re_path
from . import views


app_name = 'BNDESIntegration'
urlpatterns = [

    re_path(r"^(?P<name>operacoes|desembolsos|all)/(?P<cnpj>\d{11,14})/$",
            views.BNDESDatasetGetView.as_view(), name='search'),

    re_path(r"^(?P<name>operacoes|desembolsos|all)/(?P<cnpj>\d{11,14})/(?P<id>\d{1,4})/$",
            views.BNDESIntegrationDetailView.as_view(), name='search_detail')


]
