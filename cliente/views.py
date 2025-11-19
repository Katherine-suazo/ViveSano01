from django.shortcuts import render, redirect
from .models import Cliente
from .forms import ClienteForm


def registro_clientes(request):
    context = {}

    if request.method == 'GET':
        context['formulario_registro'] = ClienteForm
        return render(request, 'cliente/registroCliente.html', context)
    
    if request.method == 'POST':
        formulario_recibido = ClienteForm(request.POST)
        datos = formulario_recibido.data
        Cliente.objects.create(
            nombre_cliente = datos['nombre_cliente'],
            apellido_cliente = datos['apellido_cliente'],
            direccion_cliente = datos['direccion_cliente'],
            telefono_cliente = datos['telefono_cliente'],
            alergia_cliente = datos['alergia_cliente'],
        )
        print('Cliente registrado')
        return redirect('lista_clientes')
    

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/listaClientes.html', {'clientes': clientes})
