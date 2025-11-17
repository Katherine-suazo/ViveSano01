from django.urls import path
from cliente import views


urlpatterns = [
    path('', views.registro_clientes, name = 'registro_cliente'),
]