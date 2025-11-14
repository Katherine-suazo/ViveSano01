from django.db import models


class Empleado(models.Model):
    nombre_empleado = models.CharField(max_length=100, null = False, blank = False)
    apellido_empleado = models.CharField(max_length=100, null = False, blank = False)
    usuario_empleado = models.CharField(max_length=100, null = False, blank = False)
    contrasena_empleado = models.CharField(max_length=255, null = False, blank = False)
    rol_empleado = models.CharField(max_length=50, null = False, blank = False)

    def __str__(self):
        return f"{self.nombre_empleado} {self.apellido_empleado}"
    
