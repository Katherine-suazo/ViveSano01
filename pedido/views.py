from django.shortcuts import render, redirect, get_list_or_404
from .models import Pedido
from .forms import PedidoForm


def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedido/listaPedidos.html', {'pedidos': pedidos})


def crear_pedido(request):
    if request.method == 'GET':
        formulario_recibido = PedidoForm()
        return render(request, 'pedido/crearPedido.html', {'formulario_ingreso': formulario_recibido})
    
    if request.method == 'POST':
        formulario_recibido = PedidoForm(request.POST)

        if formulario_recibido.is_valid():
            # datos = formulario_recibido.changed_data
            Pedido.objects.create(
                cliente_pedido = formulario_recibido.cleaned_data['cliente_pedido'],
                estado_pedido = formulario_recibido.cleaned_data['estado_pedido'],
                fecha_entrega_pedido = formulario_recibido.cleaned_data['fecha_entrega'],
                total_pedido = formulario_recibido.cleaned_data['total_pedido'],
                empleado_pedido = formulario_recibido.cleaned_data['empleado_pedido'],
            )
            print("Pedido Realizado")
            return redirect('lista_pedidos')
        
        return render(request, 'pedido/crearPedido.html', {'formulario_ingreso': formulario_recibido})

