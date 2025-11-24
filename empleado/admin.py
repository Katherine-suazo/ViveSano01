from django.contrib import admin
from .models import Empleado


class EmpleadoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_empleado',
        'apellido_empleado',
        'usuario_empleado',
        'contrasena_empleado',
        'rol_empleado',
    )

admin.site.register(Empleado, EmpleadoAdmin)
