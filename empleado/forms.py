from django import forms


class EmpleadoForm(forms.Form):
    Usuario = forms.CharField(label = 'Usuario', required = True, widget = forms.TextInput())
    contraseña = forms.CharField(label = 'Contraseña', required = True, widget = forms.PasswordInput())

# si el usuario existe, lo enviara a la pagina principal(home.html)
# si el usuario no existe, le pedira ingresar datos de nombre, apellido y rol para registrarlo

