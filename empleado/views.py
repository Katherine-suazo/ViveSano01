from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from .models import Empleado
from .forms import EmpleadoForm, EmpleadoFormCompleto
from .decorators import empleado_login_required
from pedido.forms import ReservaForm
from pedido.models import Reserva
from producto.models import Producto
from cliente.models import Cliente


def ingreso_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)

        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            contrasena = form.cleaned_data['contrasena']

            try:
                empleado = Empleado.objects.get(usuario_empleado=usuario)
            except Empleado.DoesNotExist:
                return render(request, 'empleado/ingresoEmpleado.html', {
                    'formulario_recibido': form,
                    'error': 'Usuario o contraseña incorrectos'
                })

            if check_password(contrasena, empleado.contrasena_empleado):
                request.session['empleado_id'] = empleado.id
                return redirect('home')

            return render(request, 'empleado/ingresoEmpleado.html', {
                'formulario_recibido': form,
                'error': 'Usuario o contraseña incorrectos'
            })
    else:
        form = EmpleadoForm()
    return render(request, 'empleado/ingresoEmpleado.html', {'formulario_recibido': form})



def registro_empleado(request):
    if request.method == 'GET':
        form = EmpleadoFormCompleto()
        return render(request, 'empleado/registroEmpleado.html', {'formulario_registro': form})

    form = EmpleadoFormCompleto(request.POST)

    if form.is_valid():
        datos = form.cleaned_data
        Empleado.objects.create(
            usuario_empleado = datos['usuario'],
            contrasena_empleado = make_password(datos['contrasena']),
            nombre_empleado = datos['nombre_empleado'],
            apellido_empleado = datos['apellido_empleado'],
            rol_empleado = datos['rol_empleado']
        )
        return redirect('ingreso_empleado')

    return render(request, 'empleado/registroEmpleado.html', {'formulario_registro': form})


@empleado_login_required
def home(request):
    return render(request, 'empleado/home.html', {'perfil': request.empleado.nombre_empleado})


def cerrar_sesion(request):
    request.session.pop('empleado_id', None)
    return redirect('ingreso_empleado')


# --------------- RESERVA


@empleado_login_required
def solicitar_reserva(request):
    producto_prefill = request.GET.get('producto')

    if request.method == 'GET':
        if producto_prefill:
            try:
                producto_obj = Producto.objects.get(pk=int(producto_prefill))
            except (Producto.DoesNotExist, ValueError):
                producto_obj = None

            if producto_obj and producto_obj.stock_producto <= 0:
                form = ReservaForm(initial={'producto': producto_obj.id})
            else:
                form = ReservaForm()
                return render(request, 'empleado/solicitarReserva.html', {'formulario_registro': form, 'error': 'El producto seleccionado tiene stock disponible y no se puede reservar.'})

        else:
            form = ReservaForm()

        return render(request, 'empleado/solicitarReserva.html', {'formulario_registro': form})

    # POST
    form = ReservaForm(request.POST)
    if form.is_valid():
        datos = form.cleaned_data
        producto = datos['producto']
        cliente = datos['cliente']
        cantidad = datos['cantidad']
        comentario = datos.get('comentario')

        if producto.stock_producto > 0:
            return render(request, 'empleado/solicitarReserva.html', {'formulario_registro': form, 'error': 'No se puede reservar un producto que tiene stock disponible.'})

        Reserva.objects.create(
            producto=producto,
            cliente=cliente,
            empleado=request.empleado,
            cantidad=cantidad,
            comentario=comentario,
            estado=Reserva.ESTADO_SOLICITADO
        )

        return redirect('lista_reservas')

    return render(request, 'empleado/solicitarReserva.html', {'formulario_registro': form})


@empleado_login_required
def lista_reservas(request):
    reservas = Reserva.objects.all().order_by('-fecha_solicitud')
    return render(request, 'empleado/listaReservas.html', {'reservas': reservas})


@empleado_login_required
def confirmar_reserva(request, reserva_id):
    if request.method != 'POST':
        return redirect('lista_reservas')

    try:
        reserva = Reserva.objects.get(pk=reserva_id)
    except Reserva.DoesNotExist:
        return redirect('lista_reservas')

    if reserva.estado == Reserva.ESTADO_RESERVADO:
        return redirect('lista_reservas')

    producto = reserva.producto

    nueva_cantidad = producto.stock_producto - reserva.cantidad
    producto.stock_producto = nueva_cantidad if nueva_cantidad >= 0 else 0
    producto.save()

    reserva.estado = Reserva.ESTADO_RESERVADO
    from datetime import date
    reserva.fecha_reserva = date.today()
    reserva.save()

    return redirect('lista_reservas')


@empleado_login_required
def cancelar_reserva(request, reserva_id):
    if request.method != 'POST':
        return redirect('lista_reservas')

    try:
        reserva = Reserva.objects.get(pk=reserva_id)
    except Reserva.DoesNotExist:
        return redirect('lista_reservas')

    if reserva.estado == Reserva.ESTADO_RESERVADO:
        producto = reserva.producto
        producto.stock_producto = producto.stock_producto + reserva.cantidad
        producto.save()

    reserva.estado = Reserva.ESTADO_CANCELADO
    reserva.save()

    return redirect('lista_reservas')



@empleado_login_required
def eliminar_recerva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id = reserva_id)

    if reserva.estado == 'CANCELADO':
        reserva.delete()
        messages.success(request, 'La Reserva fue eliminada')
    else:
        messages.warning(request, 'La Reserva no puede ser eliminada')

    return redirect('lista_reservas')



# empleados = Empleado.objects.all()
# empleados = Empleado.objects.raw("select * from empleado_empleado")