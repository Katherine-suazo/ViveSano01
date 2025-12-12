from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pedido, DetallePedido
from .forms import PedidoForm, DetallePedidoForm
from producto.models import Producto
from empleado.decorators import empleado_login_required
from cliente.models import Cliente as ClienteModel   # ← IMPORT corregido


@empleado_login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedido/listaPedidos.html', {'pedidos': pedidos})


@empleado_login_required
def crear_pedido(request):

    # Verificar si hay productos con stock antes de permitir crear pedido
    productos_con_stock = Producto.objects.filter(stock_producto__gt=0)
    if not productos_con_stock.exists():
        messages.warning(request, '⚠️ No hay productos con stock disponible. Debe agregar stock a los productos primero.')
        return redirect('lista_productos')

    if request.method == 'GET':
        formulario_recibido = PedidoForm()
        return render(request, 'pedido/crearPedido.html', {
            'formulario_ingreso': formulario_recibido
        })

    if request.method == 'POST':
        formulario_recibido = PedidoForm(request.POST)

        if formulario_recibido.is_valid():
            datos = formulario_recibido.cleaned_data
            cliente = datos.get('cliente_pedido')
            producto = datos.get('producto_pedido')
            cantidad = datos.get('cantidad_producto')

            # Si NO viene cliente → usar Consumidor Final
            if not cliente:
                cliente, _ = ClienteModel.objects.get_or_create(
                    nombre_cliente='Consumidor',
                    apellido_cliente='Final',
                    defaults={
                        'direccion_cliente': '',
                        'telefono_cliente': '+56900000000',
                        'alergia_cliente': ''
                    }
                )

            # Crear el pedido
            pedido = Pedido.objects.create(
                cliente_pedido=cliente,
                estado_pedido=datos['estado_pedido'],
                fecha_entrega_pedido=datos['fecha_entrega_pedido'],
                empleado_pedido=datos['empleado_pedido'],
            )

            # Crear el detalle del pedido con el producto
            DetallePedido.objects.create(
                pedido_detalle=pedido,
                producto_detalle=producto,
                cantidad_detalle=cantidad,
                precio_unitario_detalle=producto.precio_producto
            )

            # Descontar stock del producto
            producto.stock_producto -= cantidad
            producto.save()

            # Actualizar total del pedido
            pedido.total_pedido = producto.precio_producto * cantidad
            pedido.save()

            messages.success(request, f'Pedido creado exitosamente con {cantidad} unidad(es) de {producto.nombre_producto}')
            return redirect('lista_pedidos')

        # Si no es válido, volver a mostrar el form
        return render(request, 'pedido/crearPedido.html', {
            'formulario_ingreso': formulario_recibido
        })


@empleado_login_required
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
                formulario_recibido.add_error(
                    'cantidad_detalle',
                    'No hay stock suficiente para este producto.'
                )
            else:
                # Crear detalle
                DetallePedido.objects.create(
                    pedido_detalle=pedido,
                    producto_detalle=producto,
                    cantidad_detalle=cantidad,
                    precio_unitario_detalle=producto.precio_producto
                )

                # Actualizar stock
                producto.stock_producto -= cantidad
                producto.save()

                # Actualizar total del pedido
                pedido.total_pedido += producto.precio_producto * cantidad
                pedido.save()

                return redirect('detalle_pedido', pedido_id=pedido.id)

    else:
        formulario_recibido = DetallePedidoForm()

    return render(request, 'pedido/agregarDetalle.html', {
        'pedido': pedido,
        'formulario_recibido': formulario_recibido,
    })



@empleado_login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = pedido.detallepedido_set.select_related('producto_detalle')
    return render(request, 'pedido/detallePedido.html', {
        'pedido': pedido,
        'detalles': detalles
    })



@empleado_login_required
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

