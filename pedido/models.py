from django.db import models

from cliente.models import Cliente
from empleado.models import Empleado
from producto.models import Producto

# 1. crear modelo
# 2. crear vistas
# 3. crear urls
# 4. crear plantilla


class Pedido(models.Model):
    estado_pedido = models.CharField(max_length=50, null = False, blank = False)
    fecha_creacion_pedido = models.DateField(auto_now_add=True)
    fecha_entrega_pedido = models.DateField(null = True, blank = True)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, null = False, blank = False, default = 0)
    cliente_pedido = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado_pedido = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente_pedido.nombre_cliente} {self.cliente_pedido.apellido_cliente} - Empleado: {self.empleado_pedido.nombre_empleado} {self.empleado_pedido.apellido_empleado}"
    
    class Meta():
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    @property
    def productos_resumen(self):
        detalles = self.detallepedido_set.all()
        return ", ".join(f"{d.producto_detalle.nombre_producto} (x{d.cantidad_detalle})" for d in detalles)



class DetallePedido(models.Model):
    cantidad_detalle = models.IntegerField(null = False, blank = False)
    precio_unitario_detalle = models.DecimalField(max_digits=10, decimal_places=2, null = False, blank = False)
    pedido_detalle = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto_detalle = models.ForeignKey(Producto, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"DetallePedido {self.id} - Producto: {self.producto_detalle} - Cantidad: {self.cantidad_detalle}"
    
    class Meta():
        verbose_name = "DetallePedido"
        verbose_name_plural = "DetallesPedidos"

    @property
    def subtotal(self):
        return self.cantidad_detalle * self.precio_unitario_detalle


class Reserva(models.Model):
    ESTADO_SOLICITADO = 'SOLICITADO'
    ESTADO_RESERVADO = 'RESERVADO'
    ESTADO_CANCELADO = 'CANCELADO'

    ESTADO_CHOICES = [
        (ESTADO_SOLICITADO, 'Solicitado'),
        (ESTADO_RESERVADO, 'Reservado'),
        (ESTADO_CANCELADO, 'Cancelado'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    
    cantidad = models.IntegerField(null=False, blank=False, default=1)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_reserva = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_SOLICITADO)
    comentario = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Reserva {self.id} - {self.producto.nombre_producto} x{self.cantidad} para {self.cliente} ({self.estado})"

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"