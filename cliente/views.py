from django.shortcuts import render
from .models import Cliente


def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/clientes.html', {'clientes': clientes} )

