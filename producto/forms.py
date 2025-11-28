from django import forms
from .models import Producto, CategoriaProducto


class CategoriaForm(forms.Form):
    nombre_categoria = forms.CharField(label='Nombre', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}))

class ProductoForm(forms.Form):
    nombre_producto = forms.CharField(label = 'Nombre', required = True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}))
    precio_producto = forms.DecimalField(label = 'Precio', required= True, widget= forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}))
    stock_producto = forms.IntegerField(label = 'Stock', min_value=0, required = True, widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0', 'min': '0'}))
    fecha_vencimiento_producto = forms.DateField(label = 'Fecha de vencimiento', required = True, widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    descripcion_producto = forms.CharField(label='Descripcion', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del producto'}))

    categoria_producto = forms.ModelChoiceField(queryset = CategoriaProducto.objects.all(), empty_label = "Seleccione una categoría", widget=forms.Select(attrs={'class': 'form-control'}))

    
