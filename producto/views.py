from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from .forms import ProductoForm, CategoriaForm
from .models import Producto, CategoriaProducto

# __iexact = ignora mat¿yusculas y minusculas (hola Hola HOLA) 
# __exact = el valor debe ser identico (Hola = Hola)

def ingresar_categoria(request):
    context = {}

    if request.method == 'GET':
        context['formulario_registro'] = CategoriaForm()
        return render(request, 'producto/ingresarCategoria.html', context)

    if request.method == 'POST':
        formulario_recibido = CategoriaForm(request.POST)

        if formulario_recibido.is_valid():
            nombre = formulario_recibido.cleaned_data['nombre_categoria']

            if CategoriaProducto.objects.filter(nombre_categoria__iexact = nombre).exists():
                return render(request,'producto/ingresarCategoria.html', {'formulario_registro': formulario_recibido, 'error': 'La categoría ya existe'})

            CategoriaProducto.objects.create(nombre_categoria = nombre)
            print('Categoría ingresada')
            return redirect('lista_productos')

        return render(request, 'producto/ingresarCategoria.html', {'formulario_registro': formulario_recibido})
    


def ingresar_producto(request):
    context = {}

    if request.method == 'GET':
        context['formulario_registro'] = ProductoForm
        return render(request, 'producto/ingresarProducto.html', context)
    
    if request.method == 'POST':
        formulario_recibido = ProductoForm(request.POST)

        if formulario_recibido.is_valid():
            datos = formulario_recibido.cleaned_data
            nombre_pro = datos['nombre_producto']

            if Producto.objects.filter(nombre_producto__iexact = nombre_pro).exists():
                return render(request,'producto/ingresarProducto.html', {'formulario_registro': formulario_recibido, 'error': 'El producto ya existe'})

            # categoria = CategoriaProducto.objects.get(pk=datos['categoria_producto'])
            categoria = datos['categoria_producto']
            Producto.objects.create(
                nombre_producto = datos['nombre_producto'],
                precio_producto = datos['precio_producto'],
                stock_producto = datos['stock_producto'],
                fecha_vencimiento_producto = datos['fecha_vencimiento_producto'],
                descripcion_producto = datos['descripcion_producto'],
                categoria_producto = categoria,
            )
        print("Producto registrado")
        return redirect('lista_productos')
    
    return render(request,'producto/ingresarProducto.html', {'formulario_registro': formulario_recibido})
    


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

    # if request.method == 'POST':
    if Producto.objects.filter(categoria_producto=categoria).exists():
        messages.warning(request, 'No se puede eliminar. Existen productos asociados.')
    else:
        categoria.delete()
        messages.success(request, 'La categoría se eliminó correctamente.')

    return redirect('lista_productos')


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    # if request.method == 'POST':
    producto.delete()
    return redirect('lista_productos')

        # if Producto.objects.filter(categoria_producto=categoria).exists():
        #     messages.error(request, 'No se puede eliminar. Existen productos asociados.')
        # else:
        #     categoria.delete()
        #     messages.success(request, 'La categoría se eliminó correctamente.')

    
        