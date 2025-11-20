from django.urls import path
from pedido import views


urlpatterns = [
    path('crearPedido/', views.crear_pedido, name = 'crear_pedido'),
    path('listaPedidos/', views.lista_pedidos, name = 'lista_pedidos'),
    path('<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('<int:pedido_id>/agregar-detalle/', views.agregar_detalle_pedido, name='agregar_detalle_pedido'),
    path('<int:pedido_id>/cancelar/', views.cancelar_pedido, name='cancelar_pedido'),
]

# path('eliminarCategoria/<int:id>/', views.eliminar_categoria, name = 'eliminar_categoria'),
# path('eliminarProducto/<int:id>/', views.eliminar_producto, name = 'eliminar_producto'),