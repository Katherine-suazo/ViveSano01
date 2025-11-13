from django.shortcuts import render
from .models import Empleado


def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleado/empleado.html', {'empleados': empleados})


