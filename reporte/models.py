from django.db import models

class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    tipo_reporte = models.CharField(max_length=100, null = False, blank = False)
    
