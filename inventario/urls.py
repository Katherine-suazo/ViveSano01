from django.urls import path
from . import views

urlpatterns = [
    path('inventario/', views.inventario_home, name='inventario_home'),
    path('reservas/', views.reservas_inventario, name='inventario_reservas'),
]
