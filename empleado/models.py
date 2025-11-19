from django.db import models
from django.contrib.auth.models import User

ROLES_CHOICES = [
    ('ENCARGADO_TIENDA', 'Encargado de tienda'),
    ('ENCARGADO_LOGISTICA', 'Encargado de logistica'),
    ('ATENCION_CLIENTE', 'Atencion a cliente'),
]


class Empleado(models.Model):
    nombre_empleado = models.CharField(max_length=100, null = False, blank = False)
    apellido_empleado = models.CharField(max_length=100, null = False, blank = False)
    usuario_empleado = models.CharField(max_length=100, null = False, blank = False)
    contrasena_empleado = models.CharField(max_length=255, null = False, blank = False)
    rol_empleado = models.CharField(max_length=50, choices = ROLES_CHOICES, null = False, blank = False)

    def __str__(self):
        return f"{self.nombre_empleado} {self.apellido_empleado} - {self.rol_empleado}"
    
# 1. crear modelo
# 2. crear vistas
# 3. crear urls
# 4. crear plantillas
