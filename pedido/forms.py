from django import forms
from .models import Pedido, DetallePedido
from cliente.models import Cliente
from empleado.models import Empleado
from producto.models import Producto
from datetime import date


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
    empleado_pedido = forms.ModelChoiceField(label = 'Registrado por', queryset = Empleado.objects.all(), widget = forms.Select(attrs = {'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today().isoformat()
        # set min attribute for any date fields in the form (if present)
        self.fields['fecha_entrega_pedido'].widget.attrs.update({'min': today})

    def clean_fecha_entrega_pedido(self):
        fe = self.cleaned_data.get('fecha_entrega_pedido')
        if fe and fe < date.today():
            raise forms.ValidationError('La fecha de entrega no puede ser anterior a hoy.')
        return fe

class DetallePedidoForm(forms.Form):
    producto_detalle = forms.ModelChoiceField(label = 'Producto', queryset = Producto.objects.all(), widget = forms.Select(attrs = {'class': 'form-control'}))
    cantidad_detalle = forms.IntegerField(label = 'Cantidad', min_value = 1, widget = forms.NumberInput(attrs = {'class': 'form-control'}))


class ReservaForm(forms.Form):
    cliente = forms.ModelChoiceField(label='Cliente', queryset=Cliente.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    producto = forms.ModelChoiceField(label='Producto', queryset=Producto.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    cantidad = forms.IntegerField(label='Cantidad', min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    comentario = forms.CharField(label='Comentario', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

# end of forms