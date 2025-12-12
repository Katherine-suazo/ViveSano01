from django import forms
from .models import Cliente
import re

class ClienteForm(forms.Form):
    rut_cliente = forms.CharField(
        label='RUT', 
        required=True, 
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': '12345678-9'}),
        error_messages={'required': 'El RUT es obligatorio'}
    )
    nombre_cliente = forms.CharField(label='Nombre', required=True, widget=forms.TextInput())
    apellido_cliente = forms.CharField(label='Apellido', required=True, widget=forms.TextInput())
    direccion_cliente = forms.CharField(label='Direccion',required=True,widget=forms.TextInput())
    telefono_cliente = forms.RegexField(label='Telefono',regex=r'^\+569\d{8}$',required=True,widget=forms.TextInput(attrs={'placeholder': '+56912345678'}),error_messages={'invalid': 'El teléfono debe tener formato +56912345678'})
    alergia_cliente = forms.CharField(label='Alergias',required=True,widget=forms.TextInput())


    def validar_rut_chileno(self, rut):
        """Valida formato y dígito verificador del RUT chileno"""
        # Limpiar el RUT (remover puntos y guión)
        rut_limpio = rut.replace(".", "").replace("-", "").upper()
        
        if len(rut_limpio) < 2:
            return False
        
        # Separar cuerpo y dígito verificador
        cuerpo = rut_limpio[:-1]
        dv = rut_limpio[-1]
        
        # Validar que el cuerpo sean solo números
        if not cuerpo.isdigit():
            return False
        
        # Calcular dígito verificador usando algoritmo módulo 11
        suma = 0
        multiplo = 2
        
        # Recorrer de derecha a izquierda
        for c in reversed(cuerpo):
            suma += int(c) * multiplo
            multiplo += 1
            if multiplo > 7:
                multiplo = 2
        
        resto = suma % 11
        dv_calculado = 11 - resto
        
        if dv_calculado == 11:
            dv_esperado = "0"
        elif dv_calculado == 10:
            dv_esperado = "K"
        else:
            dv_esperado = str(dv_calculado)
        
        return dv == dv_esperado


    def clean_rut_cliente(self):
        rut = self.cleaned_data.get('rut_cliente')
        
        # Validar que no esté vacío (ahora es obligatorio)
        if not rut or rut.strip() == '':
            raise forms.ValidationError("El RUT es obligatorio")
        
        rut = rut.strip().upper()  # Convertir K a mayúscula
        
        # Validar formato básico: XXXXXXXX-X o XX.XXX.XXX-X (acepta k o K al final)
        if not re.match(r'^(\d{1,2}\.?\d{3}\.?\d{3}-?[\dkK])$', rut):
            raise forms.ValidationError("Formato de RUT inválido. Use: 12345678-9 o 12.345.678-K")
        
        # Normalizar formato: sin puntos, con guión, K en mayúscula
        rut_limpio = rut.replace(".", "").upper()
        if "-" not in rut_limpio:
            rut_limpio = rut_limpio[:-1] + "-" + rut_limpio[-1]
        
        return rut_limpio


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
