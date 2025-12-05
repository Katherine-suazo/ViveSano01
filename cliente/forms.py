from django import forms
from .models import Cliente
import re

class ClienteForm(forms.Form):
    customer_id_number = forms.CharField(label='RUT / ID', required=True, max_length=10, widget=forms.TextInput(attrs={'placeholder': '19.876.543-K'}))
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


    def _normalize_id(self, value: str) -> str:
        # remove dots, hyphens and spaces, uppercase
        return ''.join(ch for ch in value if ch.isalnum()).upper()


    def _rut_valid(self, rut: str) -> bool:
        # Basic Chilean RUT validation: expects numeric body + verifier (0-9 or K)
        # rut passed normalized (no dots or hyphens), e.g. '19876543K'
        if len(rut) < 2:
            return False
        body = rut[:-1]
        dv = rut[-1].upper()
        if not body.isdigit():
            return False

        reversed_digits = map(int, reversed(body))
        factors = [2,3,4,5,6,7]
        s = 0
        factor_index = 0
        for d in reversed_digits:
            s += d * factors[factor_index]
            factor_index = (factor_index + 1) % len(factors)

        mod = 11 - (s % 11)
        if mod == 11:
            dv_calc = '0'
        elif mod == 10:
            dv_calc = 'K'
        else:
            dv_calc = str(mod)

        return dv == dv_calc


    def clean_customer_id_number(self):
        raw = self.cleaned_data.get('customer_id_number', '')
        normalized = self._normalize_id(raw)

        if not (7 <= len(normalized) <= 10):
            raise forms.ValidationError('El RUT/ID debe tener entre 7 y 10 caracteres (sin puntos ni guiones).')

        # If it looks like a Chilean RUT, validate DV
        try:
            if self._rut_valid(normalized):
                return normalized
        except Exception:
            pass

        # If rut_valid returned False, still allow if basic alphanumeric check passes
        if not normalized.isalnum():
            raise forms.ValidationError('El RUT/ID contiene caracteres inválidos.')

        return normalized


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
