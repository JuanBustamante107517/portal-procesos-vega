# backend/processes/tests.py
import pytest
from processes.models import Proceso
from rest_framework.test import APIRequestFactory
# ¡Importamos Request de DRF!
from rest_framework.request import Request
from .views import ProcesoViewSet

# --- Prueba U-B-003 ---
@pytest.mark.django_db
def test_proceso_str_representation():
    """
    PRUEBA UNITARIA U-B-003:
    Verifica que la representación en texto (__str__) del Proceso sea correcta.
    """
    proceso = Proceso.objects.create(
        titulo='Licitaciones y Convenios',
        tipo_venta='B2B',
        descripcion='Descripción de prueba...'
    )
    expected_string = "[B2B] Licitaciones y Convenios"
    assert str(proceso) == expected_string

# --- PRUEBA U-B-005  ---
@pytest.mark.django_db
def test_proceso_viewset_get_queryset_no_filter():
    """
    PRUEBA UNITARIA U-B-005:
    Verifica que get_queryset devuelva todos los procesos sin filtro.
    """
    # 1. Arrange: Creamos procesos
    Proceso.objects.create(titulo='Proceso B2B Uno', tipo_venta='B2B')
    Proceso.objects.create(titulo='Proceso B2B Dos', tipo_venta='B2B')
    Proceso.objects.create(titulo='Proceso B2C Uno', tipo_venta='B2C')

    # Simulamos la petición GET básica
    factory = APIRequestFactory()
    wsgi_request = factory.get('/fake-url-for-test/') # URL simple, no importa

    # Convertimos la petición WSGI básica en una petición DRF completa.
    # Esto añade atributos como .query_params.
    drf_request = Request(wsgi_request)
  

    # Creamos la instancia de la vista
    view = ProcesoViewSet()
    view.request = drf_request # Le inyectamos la petición DRF

    # 2. Act: Llamamos al método
    queryset = view.get_queryset()

    # 3. Assert: Comprobamos el resultado
    assert queryset.count() == 3
    # Verificamos orden alfabético por título (A-Z)
    assert queryset.first().titulo == 'Proceso B2B Dos' # Corregido: "Dos" viene antes que "Uno"
    titulos_esperados = {'Proceso B2B Uno', 'Proceso B2B Dos', 'Proceso B2C Uno'}
    titulos_obtenidos = {p.titulo for p in queryset}
    assert titulos_obtenidos == titulos_esperados

# --- (Aquí añadiremos U-B-006 después) ---
# --- PRUEBA U-B-006 ---
@pytest.mark.django_db
def test_proceso_viewset_get_queryset_with_filter():
    """
    PRUEBA UNITARIA U-B-006:
    Verifica que el filtro ?tipo_venta=B2B funcione correctamente.
    """
    # 1. Arrange: Creamos procesos, asegurando tener de ambos tipos.
    proceso_b2b_1 = Proceso.objects.create(titulo='Licitaciones', tipo_venta='B2B')
    proceso_b2b_2 = Proceso.objects.create(titulo='Campañas B2B', tipo_venta='B2B')
    proceso_b2c_1 = Proceso.objects.create(titulo='E-commerce', tipo_venta='B2C')

    # Simulamos una petición GET AHORA CON el filtro ?tipo_venta=B2B
    factory = APIRequestFactory()
    # ¡Importante! Añadimos el parámetro al .get()
    wsgi_request = factory.get('/fake-url-for-test/', {'tipo_venta': 'B2B'})

    # Convertimos a petición DRF (como en la prueba anterior)
    drf_request = Request(wsgi_request)

    # Creamos la instancia de la vista
    view = ProcesoViewSet()
    view.request = drf_request # Le inyectamos la petición con filtro

    # 2. Act: Llamamos al método get_queryset()
    queryset = view.get_queryset()

    # 3. Assert: Comprobamos que SOLO devuelva los procesos B2B
    assert queryset.count() == 2
    # Verificamos que los procesos B2C NO estén en el resultado
    assert proceso_b2c_1 not in queryset
    # Verificamos que los procesos B2B SÍ estén
    assert proceso_b2b_1 in queryset
    assert proceso_b2b_2 in queryset
    # Verificamos el orden por título
    assert queryset.first() == proceso_b2b_2 # 'Campañas B2B' va antes que 'Licitaciones'