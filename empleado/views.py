from django.shortcuts import render
from .models import Empleado
from .forms import EmpleadoForm

def lista_empleados(request):
    context = {}

    def get(self, request):
        context['formulario'] = EmpleadoForm
        empleados = Empleado.objects.all()
        # return render(request, 'empleado/ingresoEmpleado.html', {'empleados': empleados})
        return render(request, 'empleado/ingresoEmpleado.html', self.context)

    def post(self, request):
        context['formulario'] = EmpleadoForm
        empleados = Empleado.objects.all()
        return render(request, 'empleado/ingresoEmpleado.html', self.context)