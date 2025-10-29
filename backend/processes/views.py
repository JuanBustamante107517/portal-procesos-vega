# backend/processes/views.py
from rest_framework import viewsets, permissions # <-- Asegúrate que 'permissions' esté importado
from .models import Proceso
from .serializers import ProcesoSerializer

class ProcesoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Esta API devuelve la lista de Procesos.
    Permite filtrar por tipo de venta, ej: /api/processes/?tipo_venta=B2B
    """
    serializer_class = ProcesoSerializer

    # --- ¡ESTA LÍNEA ES LA CLAVE! ---
    # Debe decir EXACTAMENTE: permissions.IsAuthenticated
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        queryset = Proceso.objects.all()
        tipo_venta = self.request.query_params.get('tipo_venta')

        if tipo_venta:
            queryset = queryset.filter(tipo_venta=tipo_venta)

        return queryset.order_by('titulo')