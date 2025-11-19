from django import forms
from .models import Pedido, DetallePedido
from cliente.models import Cliente


class PedidoForm(forms.Form):

    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En proceso'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]

    estado_pedido = forms.CharField(label = 'Estado', required = True, choices = ESTADO_CHOICES, widget = forms.Select(attrs={'class': 'form-control'}))
    fecha_entrega = forms.DateTimeField(label = 'Fecha entrega', required = True, widget = forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    total_pedido = forms.DecimalField(label = 'Total', required = True, max_digits = 10, decimal_places = 2, widget = forms.NumberInput(attrs={'class': 'form-control'}))
    cliente_pedido = forms.ChoiceField(label = 'Cliente', queryset = Cliente.objects.all(), widget = forms.Select(attrs = {'class': 'form-control'}))