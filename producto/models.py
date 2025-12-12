from django.db import models


class CategoriaProducto(models.Model):
    nombre_categoria = models.CharField(max_length = 100)

    def __str__(self):
        return self.nombre_categoria


class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100, null = False, blank = False)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2, null = False, blank = False, default=0)
    stock_producto = models.IntegerField(null = False, blank = False, default=0)
    fecha_vencimiento_producto = models.DateField(null = True, blank = True)
    descripcion_producto = models.TextField(null = True, blank = True)
    categoria_producto = models.ForeignKey(CategoriaProducto, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return self.nombre_producto
    
