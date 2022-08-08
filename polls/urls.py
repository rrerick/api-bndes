from django.template import Context
from django.urls import path, re_path
from sympy import linear_eq_to_matrix
from . import views


app_name = 'polls'
urlpatterns= [
    path('home/', views.FormCnpjView.as_view(), name='form'),
    re_path(r'(?P<cnpj>\d{14})/$', views.SearchDataBase, name='search'),
    re_path(r"^home/validacao/(?P<cnpj>\d{14})/$",views.view_expiration_date, name='validador'),
    re_path(r'^home/dados/(?P<cnpj>\d{14})/$', views.busca_dados, name='buscar'),
    re_path(r'^home/(?P<cnpj>\d{14})/$', views.ListDataView.as_view(), name='informacao'),
    re_path(r'^home/search/(?P<cnpj>\d{14})/$', views.FoundCnpj, name='cnpj'),
    path('home/dados/detail/<pk>/', views.DetailOperationView.as_view(), name='detail_operation'),

]


