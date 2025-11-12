from django.db import models

from producto.models import Producto


class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    fecha_actualizacion_inventario = models.DateField(null = False, blank = False)
    almacen = models.CharField(max_length=100, null = False, blank = False)

    id_producto_inventario = models.ForeignKey(Producto, on_delete=models.CASCADE)


    def __str__(self):
        return f"Inventario {self.id_inventario} - Producto: {self.id_producto_inventario}"
