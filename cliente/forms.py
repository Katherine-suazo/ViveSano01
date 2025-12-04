from django import forms
from .models import Cliente
import re

class ClienteForm(forms.Form):
    nombre_cliente = forms.CharField(label='Nombre', required=True, widget=forms.TextInput())
    apellido_cliente = forms.CharField(label='Apellido', required=True, widget=forms.TextInput())
    direccion_cliente = forms.CharField(label='Direccion',required=True,widget=forms.TextInput())
    telefono_cliente = forms.RegexField(label='Telefono',regex=r'^\+569\d{8}$',required=True,widget=forms.TextInput(attrs={'placeholder': '+56912345678'}),error_messages={'invalid': 'El teléfono debe tener formato +56912345678'})
    alergia_cliente = forms.CharField(label='Alergias',required=True,widget=forms.TextInput())


    def clean_nombre_cliente(self):
        nombre = self.cleaned_data['nombre_cliente']

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', nombre):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        
        if len(nombre.strip()) < 2:
            raise forms.ValidationError("El nombre es demasiado corto.")
        
        return nombre


    def clean_apellido_cliente(self):
        apellido = self.cleaned_data['apellido_cliente']

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', apellido):
            raise forms.ValidationError("El apellido solo puede contener letras y espacios.")

        if len(apellido.strip()) < 2:
            raise forms.ValidationError("El apellido es demasiado corto.")

        return apellido


    def clean_direccion_cliente(self):
        direccion = self.cleaned_data['direccion_cliente']

        if len(direccion.strip()) < 5:
            raise forms.ValidationError("La dirección es demasiado corta.")

        return direccion


    def clean_alergia_cliente(self):
        alergia = self.cleaned_data['alergia_cliente']

        # opcional: evita caracteres raros
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9 ,.-]+$', alergia):
            raise forms.ValidationError("La alergia contiene caracteres inválidos.")

        return alergia
