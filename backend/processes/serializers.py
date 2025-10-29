# backend/processes/serializers.py
from rest_framework import serializers
from .models import Proceso

class ProcesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proceso
        fields = ['id', 'titulo', 'tipo_venta', 'descripcion']