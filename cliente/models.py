from django.db import models

# blank = true   permite que el campo pueda quedar vacio en los formularios
# null = true    permite que el campo pueda quedar vacio en la base de datos

class Cliente(models.Model):
    nombre_cliente = models.CharField(max_length=100, null = False, blank = False)
    apellido_cliente = models.CharField(max_length=100, null = False, blank = False)
    direccion_cliente = models.CharField(max_length=200)
    telefono_cliente = models.CharField(max_length=15)
    alergia_cliente = models.TextField(max_length=200, null = False, blank = False)

    def __str__(self):
        return f"{self.nombre_cliente} {self.apellido_cliente}"
    


# 1. crear modelo
# 2. crear vistas
# 3. crear urls
# 4. crear plantillas

