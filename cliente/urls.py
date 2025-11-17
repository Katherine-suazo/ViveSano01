from django.urls import path
from cliente import views


urlpatterns = [
    path('', views.registro_clientes, name = 'registro_cliente'),
    path('listaClientes/', views.lista_clientes, name = 'lista_clientes'),
]