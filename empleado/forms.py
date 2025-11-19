from django import forms
from .models import Empleado, ROLES_CHOICES


class EmpleadoForm(forms.Form):
    usuario = forms.CharField(label = 'Usuario', required = True, widget = forms.TextInput(attrs={'class': 'form-control'}))
    contraseña = forms.CharField(label = 'Contraseña', required = True, widget = forms.PasswordInput(attrs={'class': 'form-control'}))


class EmpleadoFormCompleto(forms.Form):
    usuario = forms.CharField(label = 'Usuario', required = True, widget = forms.TextInput(attrs={'class': 'form-control'}))
    contraseña = forms.CharField(label = 'Contraseña', required = True, widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    nombre_empleado = forms.CharField(label = 'Nombres', required = True, widget = forms.TextInput(attrs={'class': 'form-control'}))
    apellido_empleado = forms.CharField(label = 'Apellidos', required = True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    rol_empleado = forms.ChoiceField(label = 'Rol', required = True, choices = ROLES_CHOICES, widget = forms.Select(attrs={'class': 'form-control'}))


# si el usuario existe, lo enviara a la pagina principal(home.html)
# si el usuario no existe, le pedira ingresar datos de nombre, apellido y rol para registrarlo