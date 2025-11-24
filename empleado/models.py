from django.db import models

ROLES_CHOICES = [
    ('ENCARGADO_TIENDA', 'Encargado de tienda'),
    ('ENCARGADO_LOGISTICA', 'Encargado de logística'),
    ('ATENCION_CLIENTE', 'Atención al cliente'),
]

class Empleado(models.Model):
    nombre_empleado = models.CharField(max_length=100)
    apellido_empleado = models.CharField(max_length=100)
    usuario_empleado = models.CharField(max_length=100, unique=True)
    contrasena_empleado = models.CharField(max_length=255)
    rol_empleado = models.CharField(max_length=50, choices=ROLES_CHOICES)

    def __str__(self):
        return f"{self.nombre_empleado} {self.apellido_empleado} - {self.rol_empleado}"

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    
# 1. crear modelo
# 2. crear vistas
# 3. crear urls
# 4. crear plantillas
