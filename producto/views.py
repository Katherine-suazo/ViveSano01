from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
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
        return redirect('lista_productos')
    

def ingresar_producto(request):
    context = {}

    if request.method == 'GET':
        context['formulario_registro'] = ProductoForm
        return render(request, 'producto/ingresarProducto.html', context)
    
    if request.method == 'POST':
        formulario_recibido = ProductoForm(request.POST)
        datos = formulario_recibido.data
        categoria = CategoriaProducto.objects.get(pk=datos['categoria_producto'])
        Producto.objects.create(
            nombre_producto = datos['nombre_producto'],
            precio_producto = datos['precio_producto'],
            stock_producto = datos['stock_producto'],
            fecha_vencimiento_producto = datos['fecha_vencimiento_producto'],
            descripcion_producto = datos['descripcion_producto'],
            categoria_producto = categoria,
        )
        print("Producto registrado")
        # return render(request, 'producto/listaProductos.html')
        return redirect('lista_productos')
    

def lista_productos(request):
    productos = Producto.objects.all()
    categorias = CategoriaProducto.objects.all()
    return render(request, 'producto/listaProductos.html', {'productos': productos, 'categorias': categorias})


# def lista_categorias(request):
#     categorias = CategoriaProducto.objects.all()
#     return render(request, 'producto/listaProductos.html', {'categorias': categorias})
 

# def eliminar_categoria(request, id):
#     categoria = get_object_or_404(CategoriaProducto, id=id)

#     if request.method == 'POST':
#         try:
#             categoria.delete()
#             messages.success(request, 'La categoria se elimino correctamente.')
#         except IntegrityError:
#             messages.error(request, 'No se puede eliminar. Existen productos asociados.')
#     return redirect('productos/listaProductos/')
    
def eliminar_categoria(request, id):
    categoria = get_object_or_404(CategoriaProducto, id=id)

    if request.method == 'POST':
        if Producto.objects.filter(categoria_producto=categoria).exists():
            messages.error(request, 'No se puede eliminar. Existen productos asociados.')
        else:
            categoria.delete()
            messages.success(request, 'La categoría se eliminó correctamente.')

    return redirect('lista_productos')


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.delete()
    return redirect('lista_productos')

        # if Producto.objects.filter(categoria_producto=categoria).exists():
        #     messages.error(request, 'No se puede eliminar. Existen productos asociados.')
        # else:
        #     categoria.delete()
        #     messages.success(request, 'La categoría se eliminó correctamente.')

    
        