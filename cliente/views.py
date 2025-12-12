from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm
from pedido.models import Pedido
from empleado.decorators import empleado_login_required


@empleado_login_required
def registro_clientes(request):
    context = {}
    if request.method == 'GET':
        context['formulario_registro'] = ClienteForm()
        return render(request, 'cliente/registroCliente.html', context)

    if request.method == 'POST':
        formulario_recibido = ClienteForm(request.POST)
        if formulario_recibido.is_valid():
            datos = formulario_recibido.cleaned_data
            Cliente.objects.create(
                rut_cliente = datos.get('rut_cliente') or None,
                nombre_cliente = datos['nombre_cliente'],
                apellido_cliente = datos['apellido_cliente'],
                direccion_cliente = datos['direccion_cliente'],
                telefono_cliente = datos['telefono_cliente'],
                alergia_cliente = datos['alergia_cliente'],
            )
            print('Cliente registrado')
            return redirect('lista_clientes')

        # if invalid, render template with errors
        return render(request, 'cliente/registroCliente.html', {'formulario_registro': formulario_recibido})
    

@empleado_login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/listaClientes.html', {'clientes': clientes})



@empleado_login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id = id)

    if Pedido.objects.filter(cliente_pedido = cliente).exists():
        messages.warning(request, 'No se puede eliminar. Existen pedidos asociados.')
    else:
        cliente.delete()
        messages.success(request, 'El cliente se elimino correctamente.')
    return redirect('lista_clientes')


@empleado_login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id = id)

    if request.method == 'POST':
        formulario_recibido = ClienteForm(request.POST)

        if formulario_recibido.is_valid():
            datos = formulario_recibido.cleaned_data

            cliente.rut_cliente = datos.get('rut_cliente') or None
            cliente.nombre_cliente = datos['nombre_cliente']
            cliente.apellido_cliente = datos['apellido_cliente']
            cliente.direccion_cliente = datos['direccion_cliente']
            cliente.telefono_cliente = datos['telefono_cliente']
            cliente.alergia_cliente = datos['alergia_cliente']

            cliente.save()
            return redirect('lista_clientes')
        
    else:
        formulario_recibido = ClienteForm(initial = {
            'rut_cliente': cliente.rut_cliente,
            'nombre_cliente': cliente.nombre_cliente,
            'apellido_cliente': cliente.apellido_cliente,
            'direccion_cliente': cliente.direccion_cliente,
            'telefono_cliente': cliente.telefono_cliente,
            'alergia_cliente': cliente.alergia_cliente,
        })

    return render(request, 'cliente/editarcliente.html', {'formulario_recibido': formulario_recibido, 'cliente': cliente})