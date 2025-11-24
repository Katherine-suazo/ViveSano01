from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .models import Empleado
from .forms import EmpleadoForm, EmpleadoFormCompleto
from .decorators import empleado_login_required

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


# empleados = Empleado.objects.all()
# empleados = Empleado.objects.raw("select * from empleado_empleado")