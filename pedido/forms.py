from django import forms
from .models import Pedido, DetallePedido
from cliente.models import Cliente
from empleado.models import Empleado
from producto.models import Producto
from datetime import date, timedelta


class PedidoForm(forms.Form):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En proceso'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente_pedido = forms.ModelChoiceField(label='Cliente',queryset=Cliente.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))
    estado_pedido = forms.ChoiceField(label='Estado',required=True,choices=ESTADO_CHOICES,widget=forms.Select(attrs={'class': 'form-control'}))
    fecha_entrega_pedido = forms.DateField(label='Fecha entrega',required=True,widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    empleado_pedido = forms.ModelChoiceField(label='Registrado por',queryset=Empleado.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today().isoformat()
        self.fields['fecha_entrega_pedido'].widget.attrs.update({'min': today})


    def clean_fecha_entrega_pedido(self):
        fe = self.cleaned_data.get('fecha_entrega_pedido')

        if fe < date.today():
            raise forms.ValidationError('La fecha de entrega no puede ser anterior a hoy.')

        max_fecha = date.today() + timedelta(days=365)
        if fe > max_fecha:
            raise forms.ValidationError('La fecha de entrega no puede ser mayor a un año.')

        return fe


    def clean_estado_pedido(self):
        estado = self.cleaned_data.get('estado_pedido')
        estados_validos = [x[0] for x in self.ESTADO_CHOICES]
        if estado not in estados_validos:
            raise forms.ValidationError("Estado inválido.")
        return estado



class DetallePedidoForm(forms.Form):
    producto_detalle = forms.ModelChoiceField(
        label='Producto',
        queryset=Producto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    cantidad_detalle = forms.IntegerField(
        label='Cantidad',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned = super().clean()
        producto = cleaned.get("producto_detalle")
        cantidad = cleaned.get("cantidad_detalle")

        if producto and cantidad:
            if hasattr(producto, "stock_producto"):  # solo si tu modelo lo tiene
                if cantidad > producto.stock_producto:
                    raise forms.ValidationError(
                        f"Stock insuficiente. Solo quedan {producto.stock_producto} unidades."
                    )

        return cleaned


class ReservaForm(forms.Form):
    cliente = forms.ModelChoiceField(
        label='Cliente',
        queryset=Cliente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    producto = forms.ModelChoiceField(
        label='Producto',
        queryset=Producto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    cantidad = forms.IntegerField(
        label='Cantidad',
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    comentario = forms.CharField(
        label='Comentario',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    def clean_cantidad(self):
        cant = self.cleaned_data.get("cantidad")
        if cant > 1000:
            raise forms.ValidationError("Cantidad demasiado grande.")
        return cant

    def clean_comentario(self):
        com = self.cleaned_data.get("comentario", "")
        if "<script>" in com.lower():
            raise forms.ValidationError("Comentario inválido.")
        return com

    def clean(self):
        cleaned = super().clean()
        producto = cleaned.get("producto")
        cantidad = cleaned.get("cantidad")

        if producto and cantidad:
            if hasattr(producto, "stock_producto"):
                if cantidad > producto.stock_producto:
                    raise forms.ValidationError(
                        f"Stock insuficiente para reservar. Disponible: {producto.stock_producto}"
                    )
        return cleaned


