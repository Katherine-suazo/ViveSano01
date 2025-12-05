from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProductoForm, CategoriaForm
from .models import Producto, CategoriaProducto
from empleado.decorators import empleado_login_required

# __iexact = ignora mayusculas y minusculas (hola Hola HOLA) 
# __exact = el valor debe ser identico (Hola = Hola)

@empleado_login_required
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
    


@empleado_login_required
def ingresar_producto(request):
    context = {}

    if request.method == 'GET':
        # Require at least one category before allowing product creation
        categorias = CategoriaProducto.objects.all()
        if not categorias.exists():
            messages.warning(request, 'Debe crear al menos una categoría antes de ingresar productos.')
            return redirect('ingresar_categoria')

        context['formulario_registro'] = ProductoForm()
        return render(request, 'producto/ingresarProducto.html', context)
    
    if request.method == 'POST':
        formulario_recibido = ProductoForm(request.POST)

        try:
            if formulario_recibido.is_valid():
                datos = formulario_recibido.cleaned_data
                nombre_pro = datos['nombre_producto']

                if Producto.objects.filter(nombre_producto__iexact=nombre_pro).exists():
                    messages.error(request, 'El producto ya existe')
                    return render(request, 'producto/ingresarProducto.html', {'formulario_registro': formulario_recibido})

                categoria = datos['categoria_producto']

                Producto.objects.create(
                    nombre_producto=datos['nombre_producto'],
                    stock_producto=datos['stock_producto'],
                    fecha_vencimiento_producto=datos['fecha_vencimiento_producto'],
                    descripcion_producto=datos['descripcion_producto'],
                    categoria_producto=categoria,
                )
                messages.success(request, 'Producto registrado')
                print("Producto registrado")
                return redirect('lista_productos')

            # If form invalid, show errors to user
            else:
                errors = []
                for f, err in formulario_recibido.errors.items():
                    errors.append(f"{f}: {', '.join(err)}")
                messages.error(request, 'Error al crear producto: ' + ' | '.join(errors))
                return render(request, 'producto/ingresarProducto.html', {'formulario_registro': formulario_recibido})

        except Exception as e:
            messages.error(request, f'Error interno al crear producto: {e}')
            return render(request, 'producto/ingresarProducto.html', {'formulario_registro': formulario_recibido})

    return render(request, 'producto/ingresarProducto.html', {'formulario_registro': formulario_recibido})
    


@empleado_login_required
def lista_productos(request):
    productos = Producto.objects.all()
    categorias = CategoriaProducto.objects.all()
    return render(request, 'producto/listaProductos.html', {'productos': productos, 'categorias': categorias})




@empleado_login_required
def eliminar_categoria(request, id):
    categoria = get_object_or_404(CategoriaProducto, id=id)

    # if request.method == 'POST':
    if Producto.objects.filter(categoria_producto=categoria).exists():
        messages.warning(request, 'No se puede eliminar. Existen productos asociados.')
    else:
        categoria.delete()
        messages.success(request, 'La categoría se eliminó correctamente.')

    return redirect('lista_productos')


@empleado_login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id = id)
    producto.delete()
    return redirect('lista_productos')


@empleado_login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id = id)

    if request.method == 'POST':
        formulario_recibido = ProductoForm(request.POST)

        if formulario_recibido.is_valid():
            datos = formulario_recibido.cleaned_data

            producto.nombre_producto = datos['nombre_producto']
            producto.stock_producto = datos['stock_producto']
            fv = datos.get('fecha_vencimiento_producto')
            if fv is not None:
                producto.fecha_vencimiento_producto = fv
            producto.descripcion_producto = datos['descripcion_producto']
            producto.categoria_producto = datos['categoria_producto']
            
            producto.save()
            return redirect('lista_productos')
        
    else:
        formulario_recibido = ProductoForm(initial = {
            'nombre_producto': producto.nombre_producto,
            'stock_producto': producto.stock_producto,
            'fecha_vencimiento_producto': producto.fecha_vencimiento_producto,
            'descripcion_producto': producto.descripcion_producto,
            'categoria_producto': producto.categoria_producto,
        })

    return render(request, 'producto/editarProducto.html', {'formulario_recibido': formulario_recibido, 'producto': producto})

    
        

        
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