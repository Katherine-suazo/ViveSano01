from django.urls import path
from empleado import views


urlpatterns = [
    path('', views.ingreso_empleado, name = 'ingreso_empleado'),
    path('registro_empleado/', views.registro_empleado, name = 'registro_empleado'),
    path('home/', views.home, name = 'home'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('solicitar_reserva/', views.solicitar_reserva, name='solicitar_reserva'),
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reservas/confirmar/<int:reserva_id>/', views.confirmar_reserva, name='confirmar_reserva'),
    path('reservas/cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('reservas/eliminar/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('reservas/editar/<int:reserva_id>/', views.editar_reserva, name='editar_reserva')
]

