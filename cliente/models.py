from django.db import models
import uuid


def generate_customer_id():
    """Generate a 10-char uppercase hex identifier for customer_id_number."""
    return uuid.uuid4().hex[:10].upper()

# blank = true   permite que el campo pueda quedar vacio en los formularios
# null = true    permite que el campo pueda quedar vacio en la base de datos

class Cliente(models.Model):
    # Unique customer identifier (RUT/Cédula) normalized and stored without punctuation
    customer_id_number = models.CharField(max_length=10, unique=True, null=False, blank=False, default=generate_customer_id)

    nombre_cliente = models.CharField(max_length=100, null = False, blank = False)
    apellido_cliente = models.CharField(max_length=100, null = False, blank = False)
    direccion_cliente = models.CharField(max_length=200)
    telefono_cliente = models.CharField(max_length=15)
    alergia_cliente = models.TextField(max_length=200, null = False, blank = False)

    def __str__(self):
        return f"{self.nombre_cliente} {self.apellido_cliente}"
    
    class Meta():
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def clean(self):
        # Normalize customer_id_number (remove dots and hyphens, uppercase)
        if hasattr(self, 'customer_id_number') and self.customer_id_number:
            raw = self.customer_id_number
            normalized = ''.join(ch for ch in raw if ch.isalnum()).upper()
            self.customer_id_number = normalized
    


# 1. crear modelo
# 2. crear vistas
# 3. crear urls
# 4. crear plantillas

