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

    # Verificar si hay categorías antes de permitir crear producto
    if not CategoriaProducto.objects.exists():
        messages.warning(request, '⚠️ Debe crear al menos una categoría antes de ingresar productos.')
        return redirect('ingresar_categoria')

    if request.method == 'GET':
        context['formulario_registro'] = ProductoForm()
        return render(request, 'producto/ingresarProducto.html', context)
    
    if request.method == 'POST':
        formulario_recibido = ProductoForm(request.POST)

        if formulario_recibido.is_valid():
            datos = formulario_recibido.cleaned_data
            nombre_pro = datos['nombre_producto']

            if Producto.objects.filter(nombre_producto__iexact = nombre_pro).exists():
                return render(request,'producto/ingresarProducto.html', {'formulario_registro': formulario_recibido, 'error': 'El producto ya existe'})

            categoria = datos['categoria_producto']
            Producto.objects.create(
                nombre_producto = datos['nombre_producto'],
                precio_producto = datos['precio_producto'],
                stock_producto = datos['stock_producto'],
                fecha_vencimiento_producto = datos['fecha_vencimiento_producto'],
                descripcion_producto = datos['descripcion_producto'],
                categoria_producto = categoria,
            )
            messages.success(request, 'Producto registrado exitosamente')
            return redirect('lista_productos')
        
        # Si el formulario no es válido, volver a mostrar con errores
        return render(request,'producto/ingresarProducto.html', {'formulario_registro': formulario_recibido})
    
    # Fallback para otros métodos HTTP
    return redirect('lista_productos')
    


@empleado_login_required
def lista_productos(request):
    productos = Producto.objects.all()
    categorias = CategoriaProducto.objects.all()

    # Alertas de stock para productos sin stock o con stock bajo
    productos_sin_stock = productos.filter(stock_producto=0)
    productos_stock_bajo = productos.filter(stock_producto__gt=0, stock_producto__lte=5)

    if productos_sin_stock.exists():
        nombres_sin_stock = ", ".join([p.nombre_producto for p in productos_sin_stock[:5]])
        if productos_sin_stock.count() > 5:
            nombres_sin_stock += f" y {productos_sin_stock.count() - 5} más..."
        messages.warning(request, f'⚠️ Productos SIN STOCK: {nombres_sin_stock}')

    if productos_stock_bajo.exists():
        nombres_bajo = ", ".join([f"{p.nombre_producto} ({p.stock_producto})" for p in productos_stock_bajo[:5]])
        if productos_stock_bajo.count() > 5:
            nombres_bajo += f" y {productos_stock_bajo.count() - 5} más..."
        messages.info(request, f'ℹ️ Productos con STOCK BAJO: {nombres_bajo}')

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

    # Alerta de stock al cargar la página de edición
    if producto.stock_producto == 0:
        messages.warning(request, f'⚠️ ALERTA: El producto "{producto.nombre_producto}" NO tiene stock disponible (Stock: 0)')
    elif producto.stock_producto <= 5:
        messages.info(request, f'ℹ️ AVISO: El producto "{producto.nombre_producto}" tiene stock bajo (Stock: {producto.stock_producto})')

    if request.method == 'POST':
        formulario_recibido = ProductoForm(request.POST)

        if formulario_recibido.is_valid():
            datos = formulario_recibido.cleaned_data
            nuevo_stock = datos['stock_producto']

            producto.nombre_producto = datos['nombre_producto']
            producto.precio_producto = datos['precio_producto']
            producto.stock_producto = nuevo_stock
            fv = datos.get('fecha_vencimiento_producto')
            if fv is not None:
                producto.fecha_vencimiento_producto = fv
            producto.descripcion_producto = datos['descripcion_producto']
            producto.categoria_producto = datos['categoria_producto']
            
            producto.save()

            # Mensaje de éxito con alerta de stock si aplica
            if nuevo_stock == 0:
                messages.warning(request, f'Producto actualizado. ⚠️ ALERTA: Sin stock disponible.')
            elif nuevo_stock <= 5:
                messages.success(request, f'Producto actualizado. ℹ️ Stock bajo: {nuevo_stock} unidades.')
            else:
                messages.success(request, f'Producto actualizado correctamente. Stock: {nuevo_stock} unidades.')

            return redirect('lista_productos')
        
    else:
        # Formatear fecha para input type="date" (requiere formato YYYY-MM-DD)
        fecha_venc = producto.fecha_vencimiento_producto
        if fecha_venc:
            fecha_venc = fecha_venc.isoformat() if hasattr(fecha_venc, 'isoformat') else fecha_venc
        
        formulario_recibido = ProductoForm(initial = {
            'nombre_producto': producto.nombre_producto,
            'precio_producto': producto.precio_producto,
            'stock_producto': producto.stock_producto,
            'fecha_vencimiento_producto': fecha_venc,
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