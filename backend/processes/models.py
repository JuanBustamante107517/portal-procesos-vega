# backend/processes/models.py
from django.db import models

class Proceso(models.Model):
    TIPO_VENTA_CHOICES = (
        ('B2B', 'Venta B2B'),
        ('B2C', 'Venta B2C'),
    )
    
    titulo = models.CharField(max_length=200)
    tipo_venta = models.CharField(max_length=10, choices=TIPO_VENTA_CHOICES)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"[{self.tipo_venta}] {self.titulo}"