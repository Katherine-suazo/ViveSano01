from django import forms
from .models import Empleado


class EmpleadoForm(forms.Form):
    usuario = forms.CharField(label = 'Usuario', required = True, widget = forms.TextInput())
    contraseña = forms.CharField(label = 'Contraseña', required = True, widget = forms.PasswordInput())


class EmpleadoFormCompleto(forms.Form):
    usuario = forms.CharField(label = 'Usuario', required = True, widget = forms.TextInput())
    contraseña = forms.CharField(label = 'Contraseña', required = True, widget = forms.PasswordInput())
    nombre_empleado = forms.CharField(label = 'Nombres', required = True, widget = forms.TextInput())
    apellido_empleado = forms.CharField(label = 'Apellidos', required = True, widget = forms.TextInput())
    rol_empleado = forms.CharField(label = 'Rol', required = True, widget = forms.TextInput())


# si el usuario existe, lo enviara a la pagina principal(home.html)
# si el usuario no existe, le pedira ingresar datos de nombre, apellido y rol para registrarlo