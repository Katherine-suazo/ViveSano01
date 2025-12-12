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
    
    # Campos de producto
    producto_pedido = forms.ModelChoiceField(
        label='Producto',
        queryset=Producto.objects.filter(stock_producto__gt=0),  # Solo productos con stock
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    cantidad_producto = forms.IntegerField(
        label='Cantidad',
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )
    
    estado_pedido = forms.ChoiceField(label='Estado',required=True,choices=ESTADO_CHOICES,widget=forms.Select(attrs={'class': 'form-control'}))
    fecha_entrega_pedido = forms.DateField(label='Fecha entrega',required=True,widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    empleado_pedido = forms.ModelChoiceField(label='Registrado por',queryset=Empleado.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today().isoformat()
        max_date = (date.today() + timedelta(days=7)).isoformat()
        self.fields['fecha_entrega_pedido'].widget.attrs.update({'min': today, 'max': max_date})
        # Actualizar queryset de productos con stock disponible
        self.fields['producto_pedido'].queryset = Producto.objects.filter(stock_producto__gt=0)


    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto_pedido')
        cantidad = cleaned_data.get('cantidad_producto')
        
        if producto and cantidad:
            if cantidad > producto.stock_producto:
                raise forms.ValidationError(
                    f"Stock insuficiente. El producto '{producto.nombre_producto}' solo tiene {producto.stock_producto} unidades disponibles."
                )
        
        return cleaned_data


    def clean_fecha_entrega_pedido(self):
        fe = self.cleaned_data.get('fecha_entrega_pedido')

        if fe < date.today():
            raise forms.ValidationError('La fecha de entrega no puede ser anterior a hoy.')

        max_fecha = date.today() + timedelta(days=7)
        if fe > max_fecha:
            raise forms.ValidationError('La fecha de entrega no puede ser mayor a 1 semana.')

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

    fecha_entrega = forms.DateField(
        label='Fecha de entrega',
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    comentario = forms.CharField(
        label='Comentario',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today()
        min_date = (today + timedelta(days=7)).isoformat()  # Mínimo 1 semana
        max_date = (today + timedelta(days=14)).isoformat()  # Máximo 2 semanas
        self.fields['fecha_entrega'].widget.attrs.update({'min': min_date, 'max': max_date})

    def clean_fecha_entrega(self):
        fe = self.cleaned_data.get('fecha_entrega')
        today = date.today()
        
        min_fecha = today + timedelta(days=7)
        max_fecha = today + timedelta(days=14)
        
        if fe < min_fecha:
            raise forms.ValidationError('La fecha de entrega debe ser al menos 1 semana desde hoy.')
        
        if fe > max_fecha:
            raise forms.ValidationError('La fecha de entrega no puede ser mayor a 2 semanas.')
        
        return fe

    def clean_cantidad(self):
        cant = self.cleaned_data.get("cantidad")
        if cant > 500:
            raise forms.ValidationError("La cantidad máxima para reservar es 500 unidades.")
        return cant

    def clean_comentario(self):
        com = self.cleaned_data.get("comentario", "")
        if "<script>" in com.lower():
            raise forms.ValidationError("Comentario inválido.")
        return com


