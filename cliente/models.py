from django.db import models

# blank = true   permite que el campo pueda quedar vacio en los formularios
# null = true    permite que el campo pueda quedar vacio en la base de datos

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=100, null = False, blank = False)
    apellido_Cliente = models.CharField(max_length=100, null = False, blank = False)
    direccion_cliente = models.CharField(max_length=200)
    telefono_cliente = models.CharField(max_length=15)
    alergia_cliente = models.CharField(max_length=200, null = False, blank = False)

    def __str__(self):
        return f"{self.nombre_cliente} {self.apellido_Cliente}"