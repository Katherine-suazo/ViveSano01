from django import forms
from .models import Empleado, ROLES_CHOICES
import re


class EmpleadoForm(forms.Form):
    usuario = forms.CharField(label='Usuario',required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    contrasena = forms.CharField(label='Contraseña',required=True,widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))


class EmpleadoFormCompleto(forms.Form):
    usuario = forms.CharField(label='Usuario',required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    contrasena = forms.CharField(label='Contraseña',required=True,widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    nombre_empleado = forms.CharField(label='Nombres',required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}))
    apellido_empleado = forms.CharField(label='Apellidos',required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}))
    rol_empleado = forms.ChoiceField(label='Rol',required=True,choices=ROLES_CHOICES,widget=forms.Select(attrs={'class': 'form-control'}))


    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')

        # No espacios
        if " " in usuario:
            raise forms.ValidationError("El usuario no puede contener espacios.")

        # Validar solo letras, números, puntos, guion y guion bajo
        if not re.match(r'^[a-zA-Z0-9._-]+$', usuario):
            raise forms.ValidationError("El usuario contiene caracteres no permitidos.")

        # Evitar duplicados
        if Empleado.objects.filter(usuario_empleado=usuario).exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso.")

        # Mínimo 4 caracteres
        if len(usuario) < 4:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 4 caracteres.")

        return usuario


    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')

        if len(contrasena) < 6:
            raise forms.ValidationError("La contraseña debe tener mínimo 6 caracteres.")

        # Validación opcional: al menos una letra y un número
        if not re.search(r'[A-Za-z]', contrasena):
            raise forms.ValidationError("La contraseña debe contener al menos una letra.")

        if not re.search(r'\d', contrasena):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")

        return contrasena


    def clean_nombre_empleado(self):
        nombre = self.cleaned_data.get('nombre_empleado')

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', nombre):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")

        if len(nombre.strip()) < 2:
            raise forms.ValidationError("El nombre es demasiado corto.")

        return nombre


    def clean_apellido_empleado(self):
        apellido = self.cleaned_data.get('apellido_empleado')

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', apellido):
            raise forms.ValidationError("El apellido solo puede contener letras y espacios.")

        if len(apellido.strip()) < 2:
            raise forms.ValidationError("El apellido es demasiado corto.")

        return apellido


    def clean_rol_empleado(self):
        rol = self.cleaned_data.get('rol_empleado')

        roles_validos = [opcion[0] for opcion in ROLES_CHOICES]
        if rol not in roles_validos:
            raise forms.ValidationError("Rol inválido.")

        return rol


# si el usuario existe, lo enviara a la pagina principal(home.html)
# si el usuario no existe, le pedira ingresar datos de nombre, apellido y rol para registrarlo