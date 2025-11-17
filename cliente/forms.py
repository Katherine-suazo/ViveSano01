from django import forms
from .models import Cliente


class ClienteForm(forms.Form):
    nombre_cliente = forms.CharField(label = 'Nombre', required = True, widget = forms.TextInput())
    apellido_cliente = forms.CharField(label = 'Apellido', required = True, widget = forms.TextInput())
    direccion_cliente = forms.CharField(label = 'Direccion', required = True, widget = forms.TextInput())
    telefono_cliente = forms.IntegerField(label = 'Telefono', required = True, widget = forms.NumberInput())
    alergia_cliente = forms.CharField(label = 'Alergias', required = True, widget = forms.TextInput())
