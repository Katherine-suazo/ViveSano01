from django.urls import path
from producto import views

urlpatterns = [
    path('ingresarCategoria/', views.ingresar_categoria, name = 'ingresar_categoria'),
    path('ingresarProducto', views.ingresar_producto, name = 'ingresar_producto'),
    path('listaProductos/', views.lista_productos, name = 'lista_productos'),
    path('eliminarCategoria/<int:id>/', views.eliminar_categoria, name = 'eliminar_categoria'),
    path('eliminarProducto/<int:id>/', views.eliminar_producto, name = 'eliminar_producto'),
]

