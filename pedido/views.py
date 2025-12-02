from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pedido, DetallePedido
from .forms import PedidoForm, DetallePedidoForm
from producto.models import Producto
from empleado.decorators import empleado_login_required



@empleado_login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedido/listaPedidos.html', {'pedidos': pedidos})



@empleado_login_required
def crear_pedido(request):
    if request.method == 'GET':
        formulario_recibido = PedidoForm()
        return render(request, 'pedido/crearPedido.html', {'formulario_ingreso': formulario_recibido})
    
    if request.method == 'POST':
        formulario_recibido = PedidoForm(request.POST)

        if formulario_recibido.is_valid():
            datos = formulario_recibido.cleaned_data
            cliente = datos.get('cliente_pedido')
            # If no cliente provided, use a default 'Consumidor Final' guest client
            if not cliente:
                from cliente.models import Cliente as ClienteModel
                cliente, _ = ClienteModel.objects.get_or_create(
                    nombre_cliente='Consumidor',
                    apellido_cliente='Final',
                    defaults={'direccion_cliente': '', 'telefono_cliente': '', 'alergia_cliente': ''}
                )

            Pedido.objects.create(
                cliente_pedido = cliente,
                estado_pedido = datos['estado_pedido'],
                fecha_entrega_pedido = datos['fecha_entrega_pedido'],
                empleado_pedido = datos['empleado_pedido'],
            )
            print("Pedido Realizado")
            return redirect('lista_pedidos')
        
        return render(request, 'pedido/crearPedido.html', {'formulario_ingreso': formulario_recibido})



@empleado_login_required
def agregar_detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        formulario_recibido = DetallePedidoForm(request.POST)

        if formulario_recibido.is_valid():
            producto = formulario_recibido.cleaned_data['producto_detalle']
            cantidad = formulario_recibido.cleaned_data['cantidad_detalle']

            if pedido.estado_pedido == 'CANCELADO':
                messages.warning(request, 'No se pueden agregar productos, Estado CANCELADO')
                return redirect('detalle_pedido', pedido_id = pedido.id)

            else:
                if producto.stock_producto < cantidad:
                    formulario_recibido.add_error('cantidad_detalle', 'No hay stock suficiente para este producto.')
                else:
                    DetallePedido.objects.create(
                        pedido_detalle = pedido,
                        producto_detalle = producto,
                        cantidad_detalle = cantidad,
                        precio_unitario_detalle = producto.precio_producto
                    )
                    producto.stock_producto -= cantidad
                    producto.save()

                    pedido.total_pedido += producto.precio_producto * cantidad
                    pedido.save()

                    return redirect('detalle_pedido', pedido_id = pedido.id)
    else:
        formulario_recibido = DetallePedidoForm()

    return render(request, 'pedido/agregarDetalle.html', {'pedido': pedido, 'formulario_recibido': formulario_recibido,})



@empleado_login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id = pedido_id)
    detalles = pedido.detallepedido_set.select_related('producto_detalle')
    return render(request, 'pedido/detallePedido.html', {'pedido': pedido, 'detalles': detalles})


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
    pedido = get_object_or_404(Pedido, id = id)
    detalles = pedido.detallepedido_set.all()
    if detalles.exists() and pedido.estado_pedido != 'CANCELADO':
        messages.warning(request, 'No se puede eliminar el pedido: tiene productos asociados. Cancelelo primero o elimine los detalles.')
    else:
        pedido.delete()
        messages.success(request, 'El pedido fue eliminado')

    return redirect('lista_pedidos')