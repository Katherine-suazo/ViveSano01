from django.shortcuts import render, redirect
from .models import Empleado
from .forms import EmpleadoForm
from .forms import EmpleadoFormCompleto

# leer de derecha a izquierda

def ingreso_empleado(request):
    context = {}

    if request.method == 'GET':
        context['formulario_ingreso'] = EmpleadoForm
        return render(request, 'empleado/ingresoEmpleado.html', context)

    if request.method == 'POST':
        formulario_recibido = EmpleadoForm(request.POST)
        datos = formulario_recibido.data
        # empleado = Empleado.objects.raw("select * from empleado_empleado where usuario_empleado = %s", [datos['usuario']])
        empleado = Empleado.objects.filter(usuario_empleado = datos['usuario']).first()
        if empleado:
            print("existe")
            request.session['empleado_id'] = empleado.id
            return redirect('home')
        else:
            print("No existe")
            return redirect('registro_empleado')
        

def registro_empleado(request):
    context = {}

    if request.method == 'GET':
        context['formulario_registro'] = EmpleadoFormCompleto
        return render(request, 'empleado/registroEmpleado.html', context)

    if request.method == 'POST':
        formulario_recibido = EmpleadoFormCompleto(request.POST)
        datos = formulario_recibido.data
        Empleado.objects.create(
            usuario_empleado = datos['usuario'],
            contrasena_empleado = datos['contraseña'],
            nombre_empleado = datos['nombre_empleado'],
            apellido_empleado = datos['apellido_empleado'],
            rol_empleado = datos['rol_empleado'],
        )
        print("Empleado registrado")
        return redirect('home')


def home(request):
    empleado_id = request.session.get('empleado_id')
    empleado = None
    if empleado_id:
        try:
            empleado = Empleado.objects.get(pk=empleado_id)
        except Empleado.DoesNotExist:
            empleado = None

    return render(request, 'empleado/home.html',  {'perfil': empleado.nombre_empleado})

    

# empleados = Empleado.objects.all()
# empleados = Empleado.objects.raw("select * from empleado_empleado")