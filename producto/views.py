from django.shortcuts import render, redirect
from .forms import ProductoForm, CategoriaForm
from .models import Producto, CategoriaProducto


def ingresar_categoria(request):
    context = {}

    if request.method == 'GET':
        context['formulario_registro'] = CategoriaForm
        return render(request, 'producto/ingresarCategoria.html', context)

    if request.method == 'POST':
        formulario_recibido = CategoriaForm(request.POST)
        datos = formulario_recibido.data
        CategoriaProducto.objects.create(
            nombre_categoria = datos['nombre_categoria']
        )
        print('Categoria ingresada')
        return render(request, 'producto/listaProductos.html')
    

def ingresar_producto(request):
    context = {}

    if request.method == 'GET':
        context['formulario_registro'] = ProductoForm
        return render(request, 'producto/ingresarCategoria.html', context)
    
    if request.method == 'POST':
        formulario_recibido = ProductoForm(request.POST)
        datos = formulario_recibido.data
        Producto.objects.create(
            nombre_producto = datos['nombre_producto'],
            precio_producto = datos['precio_producto'],
            stock_producto = datos['stock_producto'],
            fecha_vencimiento_producto = datos['fecha_vencimiento_producto'],
            descripcion_producto = datos['descripcion_producto'],
            categoria_producto = datos['categoria_producto'],
        )
        print("Producto registrado")
        return redirect('listaProductos')
    

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'producto/listaProductos.html', {'productos': productos})


def lista_categorias(request):
    categorias = CategoriaProducto.objects.all()
    return render(request, 'producto/listaProductos.html', {'categorias': categorias})
 