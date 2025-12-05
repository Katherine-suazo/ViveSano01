from django import forms
from .models import Producto, CategoriaProducto
from datetime import date, timedelta
import re


class CategoriaForm(forms.Form):
    nombre_categoria = forms.CharField(label='Nombre',required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre de la categoría'}))


class ProductoForm(forms.Form):
    nombre_producto = forms.CharField(label='Nombre',required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre del producto'}))
    precio_producto = forms.DecimalField(label='Precio',required=True,min_value=0.01,max_value=7, widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': '0.00','step': '0.01'}))
<<<<<<< Updated upstream
    stock_producto = forms.IntegerField(label='Stock',min_value=0,max_value=500,required=True,widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': '0','min': '0'}))
    fecha_vencimiento_producto = forms.DateField(label='Fecha de vencimiento',required=False, widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    descripcion_producto = forms.CharField(label='Descripción',required=True,widget=forms.Textarea(attrs={'class': 'form-control','rows': 4,'placeholder': 'Descripción del producto'}))
=======
    stock_producto = forms.IntegerField(label='Stock',min_value=0,max_value=500, required=True, widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': '0','min': '0'}))
    fecha_vencimiento_producto = forms.DateField(label='Fecha de vencimiento', required=False, widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    descripcion_producto = forms.CharField(label='Descripción',required=True, widget=forms.Textarea(attrs={'class': 'form-control','rows': 4,'placeholder': 'Descripción del producto'}))
>>>>>>> Stashed changes
    categoria_producto = forms.ModelChoiceField(queryset=CategoriaProducto.objects.all(),empty_label="Seleccione una categoría",widget=forms.Select(attrs={'class': 'form-control'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today().isoformat()
        self.fields['fecha_vencimiento_producto'].widget.attrs.update({'min': today})


    def clean_nombre_producto(self):
        nombre = self.cleaned_data.get("nombre_producto")

        # Solo letras, números, espacios y tildes
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]+$', nombre):
            raise forms.ValidationError("El nombre contiene caracteres inválidos.")

        if len(nombre.strip()) < 2:
            raise forms.ValidationError("El nombre es demasiado corto.")

        return nombre


    def clean_descripcion_producto(self):
        desc = self.cleaned_data.get("descripcion_producto")

        # Evitar scripts o código malicioso
        if "<script>" in desc.lower():
            raise forms.ValidationError("La descripción no puede contener código.")

        if len(desc.strip()) < 5:
            raise forms.ValidationError("La descripción es demasiado corta.")

        return desc


    def clean_fecha_vencimiento_producto(self):
        fv = self.cleaned_data.get('fecha_vencimiento_producto')

        # Si el campo es opcional y viene vacío, lo dejamos pasar
        if not fv:
            return fv

        # Validación de fecha mínima
        if fv < date.today():
            raise forms.ValidationError('La fecha de vencimiento no puede ser anterior a hoy.')

        # Validación de fecha máxima (5 años hacia adelante)
        max_fv = date.today() + timedelta(days=5 * 365)
        if fv > max_fv:
            raise forms.ValidationError("La fecha de vencimiento no puede exceder 5 años en el futuro.")

        return fv


    def clean_categoria_producto(self):
        categoria = self.cleaned_data.get("categoria_producto")
        if categoria is None:
            raise forms.ValidationError("Debe seleccionar una categoría válida.")
        return categoria

    
