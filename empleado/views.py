from django.shortcuts import render, redirect
from .models import Empleado
from .forms import EmpleadoForm
from .forms import EmpleadoFormCompleto

# leer de derecha a izquierda

def lista_empleados(request):
    print(request)
    context = {}

    if request.method == 'GET':
        context['formulario_ingreso'] = EmpleadoForm
        return render(request, 'empleado/ingresoEmpleado.html', context)

    if request.method == 'POST':
        formulario_recibido = EmpleadoForm(request.POST)
        datos = formulario_recibido.data
        empleado = Empleado.objects.raw("select * from empleado_empleado where usuario_empleado = %s", [datos['usuario']])
        if empleado:
            print("existe")
            return redirect('home')
        else:
            print("No existe")
            return redirect('continuar_registro')
    

def continuar_registro(request):
    # hacer get
    context = {}
    context['formulario_registro'] = EmpleadoFormCompleto
    return render(request, 'empleado/registroEmpleado.html', context)

    #post
    # formulario_recibido = EmpleadoForm(request.POST)
    # datos = formulario_recibido.data
    # Empleado.objects.create(
        #     usuario_empleado = datos['usuario'],
        #     contrasena_empleado = datos['contraseña'],
        #     nombre_empleado = datos['nombre_empleado'],
        #     apellido_empleado = datos['apellido_empleado'],
        #     rol_empleado = datos['rol_empleado'],
        # )
        # return redirect('home')


def home(request):
    return render(request, 'empleado/home.html')



        # empleados = Empleado.objects.all()
        # empleados = Empleado.objects.raw("select * from empleado_empleado")
    