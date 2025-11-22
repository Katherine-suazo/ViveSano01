from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
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

        if formulario_recibido.is_valid():
            datos = formulario_recibido.cleaned_data
            # empleado = Empleado.objects.filter(usuario_empleado = datos['usuario']).first()
            empleado = authenticate(request, usuario_empleado = datos['usuario_empleado'], contrasena_empleado = datos['contrasena_empleado'])

            if empleado is not None:
                if empleado.is_active:
                    login(request, empleado)
                    return HttpResponse(['Empleado autenticado'])
                # request.session['empleado_id'] = empleado.id
                # return redirect('home')
            else:
                return HttpResponse('El usuario no esta activo')
            
        else:
            return HttpResponse('La informacion no es correcta')
        
    else:
        formulario_recibido = EmpleadoForm()
        return render(request, 'empleado/ingresoEmpleado.html', {'formulario_recibido': formulario_recibido})


        

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