# backend/processes/tests.py
import pytest
from processes.models import Proceso
from rest_framework.test import APIRequestFactory
# ¡Importamos Request de DRF!
from rest_framework.request import Request
from .views import ProcesoViewSet
# --- ¡AÑADE ESTOS IMPORTS NUEVOS! ---
from django.contrib.auth.models import User
from users.models import Profile
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

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


# ... (mis 3 pruebas unitarias U-B-003, 005, 006)...

# --- ¡NUEVA PRUEBA DE INTEGRACIÓN I-003! ---
@pytest.mark.django_db
def test_integration_I003_authorized_data_access(client):
    """
    PRUEBA DE INTEGRACIÓN I-003: Acceso Autorizado a Datos Protegidos.
    Verifica que un usuario logueado pueda ver la lista de procesos.
    """
    # 1. Arrange: 
    #    Creamos el usuario 'admin' y le asignamos su rol.
    user = User.objects.create_user(username='admin', password='CHOcho2002')
    profile = Profile.objects.get(user=user)
    profile.role = 'ADMIN'
    profile.save()

    # Creamos los datos que queremos obtener (los procesos B2B)
    Proceso.objects.create(titulo='Licitaciones', tipo_venta='B2B')
    Proceso.objects.create(titulo='Campañas B2B', tipo_venta='B2B')
    # Y un dato que NO queremos obtener
    Proceso.objects.create(titulo='E-commerce', tipo_venta='B2C')

    # Obtenemos un token de acceso para este usuario
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)

    # Obtenemos la URL de la API (usando el 'basename' que definimos)
    # Esto genera la URL: /api/processes/
    url = reverse('proceso-list') 
    # ¡Añadimos el filtro que queremos probar!
    url_con_filtro = f"{url}?tipo_venta=B2B" 

    # 2. Act: 
    #    Usamos el 'client' para simular un GET, pero esta vez
    #    pasamos la cabecera de autorización con el token.
    response = client.get(
        url_con_filtro, 
        HTTP_AUTHORIZATION=f'Bearer {token}'
    )

    # 3. Assert: 
    #    Verificamos que el Backend nos dio los datos.

    # 3.1: ¿El código de estado fue 200 OK?
    assert response.status_code == 200

    # 3.2: ¿La respuesta contiene 2 resultados (solo los B2B)?
    assert len(response.data) == 2

    # 3.3: ¿Los títulos son los correctos?
    titulos_obtenidos = {proceso['titulo'] for proceso in response.data}
    assert titulos_obtenidos == {'Licitaciones', 'Campañas B2B'}

# --- ¡NUEVA PRUEBA DE INTEGRACIÓN I-004! ---
@pytest.mark.django_db
def test_integration_I004_unauthorized_no_token(client):
    """
    PRUEBA DE INTEGRACIÓN I-004: Acceso Denegado Sin Token.
    Verifica que la API /api/processes/ rechace a un usuario sin token.
    """
    # 1. Arrange: 
    #    Obtenemos la URL de la API. No necesitamos crear datos ni
    #    usuarios, solo queremos probar el acceso a la puerta.
    url = reverse('proceso-list') # URL: /api/processes/
    url_con_filtro = f"{url}?tipo_venta=B2B"

    # 2. Act: 
    #    Simulamos un GET, pero esta vez NO pasamos la cabecera
    #    HTTP_AUTHORIZATION. Estamos "tocando la puerta" sin token.
    response = client.get(url_con_filtro)

    # 3. Assert: 
    #    Verificamos que el Backend nos rechazó con 401.

    # 3.1: ¿El código de estado fue 401 Unauthorized?
    assert response.status_code == 401

# --- ¡NUEVA PRUEBA DE INTEGRACIÓN I-005! ---
@pytest.mark.django_db
def test_integration_I005_forbidden_insufficient_role(client):
    """
    PRUEBA DE INTEGRACIÓN I-005: Acceso Denegado por Rol Insuficiente.
    Verifica que la API rechace a un usuario con rol 'CAJERO'.
    """
    # 1. Arrange: 
    #    Creamos un usuario 'cajero' y le asignamos su rol.
    user = User.objects.create_user(username='test_cajero', password='password123')
    profile = Profile.objects.get(user=user)
    profile.role = 'CAJERO' # ¡Rol insuficiente!
    profile.save()

    # Obtenemos un token de acceso para este cajero
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)

    # Obtenemos la URL de la API
    url = reverse('proceso-list') # URL: /api/processes/
    url_con_filtro = f"{url}?tipo_venta=B2B"

    # 2. Act: 
    #    Simulamos un GET con el token del CAJERO.
    response = client.get(
        url_con_filtro, 
        HTTP_AUTHORIZATION=f'Bearer {token}'
    )

    # 3. Assert: 
    #    Verificamos que el Backend nos rechazó con 403 Forbidden.

    # 3.1: ¿El código de estado fue 403 Forbidden?
    assert response.status_code == 403



















