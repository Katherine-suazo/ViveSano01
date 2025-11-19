from django.shortcuts import render, redirect
from .models import Pedido
from .forms import PedidoForm


def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedido/listaPedidos.html', {'pedidos': pedidos})


def crear_pedido(request):
    context = {}

    if request.method == 'GET':
        context['formulario_ingreso'] = PedidoForm
        return render(request, 'pedido/crearPedido.html', context)
    
    if request.method == 'POST':
        formulario_recibido = PedidoForm(request.POST)
        datos = formulario_recibido.data
        Pedido

