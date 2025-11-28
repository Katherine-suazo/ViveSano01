from django.shortcuts import render, redirect
from producto.models import Producto
from pedido.models import Reserva
from empleado.decorators import empleado_login_required


@empleado_login_required
def inventario_home(request):
	productos = Producto.objects.all()
	return render(request, 'inventario/inventario.html', {'productos': productos})


@empleado_login_required
def reservas_inventario(request):
	reservas = Reserva.objects.all().order_by('-fecha_solicitud')
	# reservas = Reserva.objects.raw("select id,fecha_solicitud,fecha_reserva,estado from empleado_empleado")
	return render(request, 'empleado/listaReservas.html', {'reservas': reservas})
