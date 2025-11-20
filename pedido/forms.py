from django import forms
from .models import Pedido, DetallePedido
from cliente.models import Cliente
from empleado.models import Empleado


class PedidoForm(forms.Form):

    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En proceso'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]
    cliente_pedido = forms.ModelChoiceField(label = 'Cliente', queryset = Cliente.objects.all(), widget = forms.Select(attrs = {'class': 'form-control'}))
    estado_pedido = forms.ChoiceField(label = 'Estado', required = True, choices = ESTADO_CHOICES, widget = forms.Select(attrs={'class': 'form-control'}))
    fecha_entrega_pedido = forms.DateField(label = 'Fecha entrega', required = True, widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    total_pedido = forms.DecimalField(label = 'Total', required = True, max_digits = 10, decimal_places = 2, widget = forms.NumberInput(attrs={'class': 'form-control'}))
    empleado_pedido = forms.ModelChoiceField(label = 'Registrado por', queryset = Empleado.objects.all(), widget = forms.Select(attrs = {'class': 'form-control'}))