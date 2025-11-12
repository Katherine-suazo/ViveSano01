from django.urls import path
from cliente import views

urlpatterns = [
    path('', views.lista_clientes, name = 'lista_clientes')
]