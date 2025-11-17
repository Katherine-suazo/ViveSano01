from django.urls import path
from producto import views

urlpatterns = [
    path('ingresarCategoria/', views.ingresar_categoria, name = 'ingresar_categoria'),
    path('', views.ingresar_producto, name = 'ingresar_producto'),
    path('listaProductos/', views.lista_productos, name='lista_productos'),
]
