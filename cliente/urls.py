from django.urls import path
from cliente import views


urlpatterns = [
    path('', views.registro_clientes, name = 'registro_cliente'),
    path('listaClientes/', views.lista_clientes, name = 'lista_clientes'),
    path('eliminarCliente/<int:id>', views.eliminar_cliente, name = 'eliminar_cliente'),
    path('editarCliente/<int:id>', views.editar_cliente, name = 'editar_cliente'),
    path('detalleCliente/<int:id>/', views.editar_cliente, name='detalle_cliente'),
]