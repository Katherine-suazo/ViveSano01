from django import forms
from .models import Producto, CategoriaProducto


class CategoriaForm(forms.Form):
    nombre_categoria = forms.CharField(label='Nombre', required=True, widget=forms.TextInput())

class ProductoForm(forms.Form):
    nombre_producto = forms.CharField(label = 'Nombre', required = True, widget = forms.TextInput())
    precio_producto = forms.DecimalField(label = 'Precio', required= True, widget= forms.NumberInput())
    stock_producto = forms.IntegerField(label = 'Stock', required = True, widget = forms.NumberInput())
    fecha_vencimiento_producto = forms.DateField(label = 'Fecha de venc (aaaa-mm-dd)', required = True, widget = forms.DateInput())
    descripcion_producto = forms.CharField(label='Descripcion', required=True, widget=forms.TextInput())

    categoria_producto = forms.ModelChoiceField(queryset = CategoriaProducto.objects.all(), empty_label = "Seleccione una categoría")

    
