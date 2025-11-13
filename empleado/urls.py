from django.urls import path
from empleado import views


urlpatterns = [
    path('', views.lista_empleados, name = 'lista_empleados')
]