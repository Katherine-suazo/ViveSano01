from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pedido, DetallePedido
from .forms import PedidoForm, DetallePedidoForm
from producto.models import Producto, CategoriaProducto
from empleado.decorators import empleado_login_required
from cliente.models import Cliente as ClienteModel   #  IMPORT corregido
from functools import wraps


def require_categoria(view_func):
    """Decorator that ensures at least one CategoriaProducto exists.

    If no category exists, redirect the user to create one with a warning message.
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not CategoriaProducto.objects.exists():
            messages.warning(request, 'Debe crear al menos una categoría antes de acceder a Pedidos.')
            return redirect('ingresar_categoria')
        return view_func(request, *args, **kwargs)

    return _wrapped


@empleado_login_required
@require_categoria
def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedido/listaPedidos.html', {'pedidos': pedidos})


@empleado_login_required
@require_categoria
def crear_pedido(request):
    # GET: show create form (cliente selection required) and small detalle form to add the first product
    if request.method == 'GET':
        formulario_recibido = PedidoForm()
        detalle_form = DetallePedidoForm()
        has_clients = ClienteModel.objects.exists()
        return render(request, 'pedido/crearPedido.html', {
            'formulario_ingreso': formulario_recibido,
            'detalle_form': detalle_form,
            'has_clients': has_clients,
        })

    # POST: handle creating pedido and its first detalle in one request
    if request.method == 'POST':
        formulario_recibido = PedidoForm(request.POST)
        detalle_form = DetallePedidoForm(request.POST)

        has_clients = ClienteModel.objects.exists()

        if not has_clients:
            messages.warning(request, 'Debe crear al menos un cliente antes de generar pedidos.')
            return redirect('registro_clientes')

        if formulario_recibido.is_valid() and detalle_form.is_valid():
            datos = formulario_recibido.cleaned_data
            cliente = datos.get('cliente_pedido')

            # create pedido
            pedido = Pedido.objects.create(
                cliente_pedido=cliente,
                estado_pedido=datos['estado_pedido'],
                fecha_entrega_pedido=datos['fecha_entrega_pedido'],
                empleado_pedido=datos['empleado_pedido'],
            )

            # create detalle and update stock/total
            producto = detalle_form.cleaned_data['producto_detalle']
            cantidad = detalle_form.cleaned_data['cantidad_detalle']

            # validate stock
            if producto.stock_producto < cantidad:
                messages.error(request, f'Stock insuficiente para el producto "{producto.nombre_producto}". Disponible: {producto.stock_producto}.')
                # remove created pedido to avoid orphan
                pedido.delete()
                return render(request, 'pedido/crearPedido.html', {
                    'formulario_ingreso': formulario_recibido,
                    'detalle_form': detalle_form,
                    'has_clients': has_clients,
                })

            from decimal import Decimal
            precio_unitario = getattr(producto, 'precio_producto', None) or Decimal('0.00')

            DetallePedido.objects.create(
                pedido_detalle=pedido,
                producto_detalle=producto,
                cantidad_detalle=cantidad,
                precio_unitario_detalle=precio_unitario
            )

            producto.stock_producto -= cantidad
            producto.save()

            pedido.total_pedido += precio_unitario * cantidad
            pedido.save()

            messages.success(request, 'Pedido creado con su primer producto.')
            return redirect('detalle_pedido', pedido_id=pedido.id)

        # If either form invalid, show errors
        return render(request, 'pedido/crearPedido.html', {
            'formulario_ingreso': formulario_recibido,
            'detalle_form': detalle_form,
            'has_clients': has_clients,
        })


@empleado_login_required
@require_categoria
def agregar_detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        formulario_recibido = DetallePedidoForm(request.POST)

        if formulario_recibido.is_valid():
            producto = formulario_recibido.cleaned_data['producto_detalle']
            cantidad = formulario_recibido.cleaned_data['cantidad_detalle']

            # No se puede modificar si está cancelado
            if pedido.estado_pedido == 'CANCELADO':
                messages.warning(request, 'No se pueden agregar productos, el pedido está CANCELADO.')
                return redirect('detalle_pedido', pedido_id=pedido.id)

            # Validar stock
            if producto.stock_producto < cantidad:
                # Show a clear notification to the user when there's no stock
                messages.error(request, f'No hay stock suficiente para el producto "{producto.nombre_producto}". Disponible: {producto.stock_producto}.')
                formulario_recibido.add_error(
                    'cantidad_detalle',
                    'No hay stock suficiente para este producto.'
                )
                return render(request, 'pedido/agregarDetalle.html', {
                    'pedido': pedido,
                    'formulario_recibido': formulario_recibido,
                })
            else:
                # Crear detalle
                # When product price is not tracked, store precio_unitario_detalle as 0 (or product price if later available)
                from decimal import Decimal
                precio_unitario = getattr(producto, 'precio_producto', None) or Decimal('0.00')

                DetallePedido.objects.create(
                    pedido_detalle=pedido,
                    producto_detalle=producto,
                    cantidad_detalle=cantidad,
                    precio_unitario_detalle=precio_unitario
                )

                # Actualizar stock
                producto.stock_producto -= cantidad
                producto.save()

                # Actualizar total del pedido (uses the detalle's unit price)
                pedido.total_pedido += precio_unitario * cantidad
                pedido.save()

                return redirect('detalle_pedido', pedido_id=pedido.id)

    else:
        formulario_recibido = DetallePedidoForm()

    return render(request, 'pedido/agregarDetalle.html', {
        'pedido': pedido,
        'formulario_recibido': formulario_recibido,
    })



@empleado_login_required
@require_categoria
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = pedido.detallepedido_set.select_related('producto_detalle')
    return render(request, 'pedido/detallePedido.html', {
        'pedido': pedido,
        'detalles': detalles
    })



@empleado_login_required
@require_categoria
def actualizar_estado_pedido(request, pedido_id):

    if request.method != 'POST':
        return redirect('detalle_pedido', pedido_id=pedido_id)

    pedido = get_object_or_404(Pedido, id=pedido_id)
    nuevo_estado = request.POST.get('estado')

    if nuevo_estado:
        pedido.estado_pedido = nuevo_estado
        pedido.save()

    return redirect('detalle_pedido', pedido_id=pedido.id)


@empleado_login_required
@require_categoria
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = pedido.detallepedido_set.select_related('producto_detalle')

    for d in detalles:
        producto = d.producto_detalle
        producto.stock_producto += d.cantidad_detalle
        producto.save()

    pedido.estado_pedido = 'CANCELADO'
    pedido.total_pedido = 0
    pedido.save()

    return redirect('detalle_pedido', pedido_id=pedido.id)


@empleado_login_required
@require_categoria
def eliminar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    detalles = pedido.detallepedido_set.all()

    if detalles.exists() and pedido.estado_pedido != 'CANCELADO':
        messages.warning(
            request,
            'No se puede eliminar el pedido: tiene productos asociados. '
            'Cancélelo primero o elimine los detalles.'
        )
    else:
        pedido.delete()
        messages.success(request, 'El pedido fue eliminado.')

    return redirect('lista_pedidos')



@empleado_login_required
@require_categoria
def editar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)

    if request.method == 'POST':
        form = PedidoForm(request.POST)

        if form.is_valid():

            pedido.cliente_pedido = form.cleaned_data['cliente_pedido']
            pedido.estado_pedido = form.cleaned_data['estado_pedido']
            pedido.fecha_entrega_pedido = form.cleaned_data['fecha_entrega_pedido']
            pedido.empleado_pedido = form.cleaned_data['empleado_pedido']

            pedido.save()
            messages.success(request, "El pedido fue actualizado correctamente.")
            return redirect('lista_pedidos')

    else:
        form = PedidoForm(initial={
            'cliente_pedido': pedido.cliente_pedido,
            'estado_pedido': pedido.estado_pedido,
            'fecha_entrega_pedido': pedido.fecha_entrega_pedido,
            'empleado_pedido': pedido.empleado_pedido,
        })

    return render(request, 'pedido/editarPedido.html', {
        'formulario_recibido': form,
        'pedido': pedido,
    })

