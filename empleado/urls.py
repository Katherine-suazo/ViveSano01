from django.urls import path
from empleado import views


urlpatterns = [
    path('', views.ingreso_empleado, name = 'ingreso_empleado'),
    path('registro_empleado/', views.registro_empleado, name = 'registro_empleado'),
    path('home/', views.home, name = 'home')
]