from django.urls import path
from pedido import views


urlpatterns = [
    path('crearPedido/', views.crear_pedido, name = 'crear_pedido'),
    path('listaPedidos/', views.lista_pedidos, name = 'lista_pedidos'),
]

# path('eliminarCategoria/<int:id>/', views.eliminar_categoria, name = 'eliminar_categoria'),
# path('eliminarProducto/<int:id>/', views.eliminar_producto, name = 'eliminar_producto'),