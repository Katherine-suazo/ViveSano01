from django.db import models


class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100, null = False, blank = False)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2, null = False, blank = False)
    stock_producto = models.IntegerField(null = False, blank = False)
    fecha_vencimiento_producto = models.DateField(null = True, blank = True)
    descripcion_producto = models.TextField(null = True, blank = True)

    def __str__(self):
        return f"{self.nombre_producto} - Precio: {self.precio_producto}"
