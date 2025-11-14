from django.urls import path
from empleado import views


urlpatterns = [
    path('', views.lista_empleados, name = 'lista_empleados'),
    path('/continuar_registro', views.continuar_registro, name = 'continuar_registro'),
    path('/home', views.home, name = 'home')
]