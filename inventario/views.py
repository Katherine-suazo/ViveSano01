from django.shortcuts import render, redirect
from producto.models import Producto
from pedido.models import Reserva
from empleado.decorators import empleado_login_required


@empleado_login_required
def inventario_home(request):
	"""Mostrar un resumen del inventario (productos)."""
	productos = Producto.objects.all()
	return render(request, 'inventario/inventario.html', {'productos': productos})


@empleado_login_required
def reservas_inventario(request):
	"""Mostrar la lista de reservas dentro del módulo de inventario.

	Reutiliza la plantilla de empleado para lista de reservas.
	"""
	reservas = Reserva.objects.all().order_by('-fecha_solicitud')
	return render(request, 'empleado/listaReservas.html', {'reservas': reservas})
