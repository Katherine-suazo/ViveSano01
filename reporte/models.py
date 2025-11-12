from django.db import models

from empleado.models import Empleado

class Reporte(models.Model):
    tipo_reporte = models.CharField(max_length = 100, null = False, blank = False)
    fecha_generacion_reporte = models.DateTimeField(auto_now_add = True)
    contenido = models.TextField(null = True, blank = True)

    empleado_reporte = models.ForeignKey(Empleado, on_delete = models.CASCADE)

    def __str__(self):
        return f"Reporte {self.id} - Contenido: {self.contenido}"

