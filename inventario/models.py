from django.db import models

from producto.models import Producto


class Inventario(models.Model):
    fecha_actualizacion_inventario = models.DateField(null = False, blank = False)
    almacen = models.CharField(max_length=100, null = False, blank = False)

    producto_inventario = models.ForeignKey(Producto, on_delete=models.CASCADE)


    def __str__(self):
        return f"Inventario {self.id} - Producto: {self.producto_inventario}"
