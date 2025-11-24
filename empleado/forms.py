from django import forms
from .models import Empleado, ROLES_CHOICES


class EmpleadoForm(forms.Form):
    usuario = forms.CharField(label='Usuario', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    contrasena = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))


class EmpleadoFormCompleto(forms.Form):
    usuario = forms.CharField(label='Usuario', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    contrasena = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    nombre_empleado = forms.CharField(label='Nombres', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}))
    apellido_empleado = forms.CharField(label='Apellidos', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}))
    rol_empleado = forms.ChoiceField(label='Rol',  required=True, choices=ROLES_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')
        if Empleado.objects.filter(usuario_empleado=usuario).exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso.")
        return usuario

    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        if contrasena and len(contrasena) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return contrasena

# si el usuario existe, lo enviara a la pagina principal(home.html)
# si el usuario no existe, le pedira ingresar datos de nombre, apellido y rol para registrarlo