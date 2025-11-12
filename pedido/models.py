from django.db import models

from cliente.models import Cliente
from empleado.models import Empleado
from producto.models import Producto


class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    estado_pedido = models.CharField(max_length=50, null = False, blank = False)
    fecha_creacion_pedido = models.DateTimeField(auto_now_add=True)
    fecha_entrega_pedido = models.DateTimeField(null = True, blank = True)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, null = False, blank = False)

    cliente_pedido = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado_pedido = models.ForeignKey(Empleado, on_delete=models.CASCADE)


    def __str__(self):
        return f"Pedido {self.id_pedido} - Cliente: {self.cliente_pedido.nombre_cliente} {self.cliente_pedido.apellido_Cliente} - Empleado: {self.empleado_pedido.nombre_empleado} {self.empleado_pedido.apellido_empleado}"
    


class DetallePedido(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    cantidad_detalle = models.IntegerField(null = False, blank = False)
    precio_unitario_detalle = models.DecimalField(max_digits=10, decimal_places=2, null = False, blank = False)

    id_pedido_detalle = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_producto_detalle = models.ForeignKey(Producto, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"DetallePedido {self.id_detalle_pedido} - Producto: {self.id_producto_detalle} - Cantidad: {self.cantidad_detalle}"