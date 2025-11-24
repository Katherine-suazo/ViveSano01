from django.contrib import admin
from .models import Cliente


class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_cliente',
        'apellido_cliente',
        'direccion_cliente',
        'telefono_cliente',
        'alergia_cliente'

    )

admin.site.register(Cliente, ClienteAdmin)


