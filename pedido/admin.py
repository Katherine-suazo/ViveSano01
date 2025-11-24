from django.contrib import admin
from .models import Pedido, DetallePedido


class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'cliente_pedido',
        'estado_pedido',
        'fecha_creacion_pedido',
        'fecha_entrega_pedido',
        'total_pedido',
        'empleado_pedido',
    )

class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = (
        'cantidad_detalle',
        'precio_unitario_detalle',
        'pedido_detalle',
        'producto_detalle',
    )

admin.site.register(Pedido, PedidoAdmin)
admin.site.register(DetallePedido, DetallePedidoAdmin)

