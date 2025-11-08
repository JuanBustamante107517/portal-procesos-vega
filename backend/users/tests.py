# backend/users/tests.py
import pytest
from django.contrib.auth.models import User
from users.models import Profile # Asegúrate que Profile esté importado
# ¡Importamos nuestro serializador de token personalizado!
from users.serializers import MyTokenObtainPairSerializer
from django.urls import reverse # Herramienta para obtener URLs

# --- Prueba U-B-001 (Ya la teníamos) ---
@pytest.mark.django_db
def test_profile_default_role():
    """
    PRUEBA UNITARIA U-B-001:
    Verifica que el rol por defecto de un Profile recién creado sea 'CAJERO'.
    """
    # 1. Arrange: Creamos un usuario nuevo
    user = User.objects.create_user(username='test_cajero', password='password123')

    # 2. Act: Obtenemos el perfil que se debió crear automáticamente
    #    Usamos .get() que fallará si el perfil no existe (¡buena prueba!)
    profile = Profile.objects.get(user=user)

    # 3. Assert: Comprobamos si el rol es el esperado
    assert profile.role == 'CAJERO'

# --- ¡NUEVA PRUEBA U-B-002! ---
@pytest.mark.django_db
def test_profile_str_representation():
    """
    PRUEBA UNITARIA U-B-002:
    Verifica que la representación en texto (__str__) del Profile sea correcta.
    """
    # 1. Arrange: Creamos un usuario y le asignamos un rol específico.
    user = User.objects.create_user(username='test_jefe', password='password123')
    profile = Profile.objects.get(user=user) # Obtenemos su perfil
    profile.role = 'JEFE' # Cambiamos el rol (por defecto era CAJERO)
    profile.save() # Guardamos el cambio

    # 2. Act: Llamamos a la función str() sobre el objeto profile.
    profile_string = str(profile)

    # 3. Assert: Comprobamos si la cadena es la esperada.
    #    Usamos get_role_display() para obtener el nombre legible del rol ('Jefe').
    expected_string = f"{user.username} - {profile.get_role_display()}"
    assert profile_string == expected_string
    # También podemos verificar contra el valor directo si quisiéramos:
    # assert profile_string == "test_jefe - Jefe"

    # --- ¡NUEVA PRUEBA U-B-004! ---
@pytest.mark.django_db
def test_token_payload_contains_role_and_username():
    """
    PRUEBA UNITARIA U-B-004:
    Verifica que el payload del token JWT contenga username y role.
    """
    # 1. Arrange: Creamos un usuario con un rol específico.
    user = User.objects.create_user(username='test_admin', password='password123')
    profile = Profile.objects.get(user=user)
    profile.role = 'ADMIN'
    profile.save()

    # 2. Act: Usamos nuestro serializador personalizado para obtener el token.
    #    El método get_token() es el que modifica el payload.
    serializer = MyTokenObtainPairSerializer()
    token = serializer.get_token(user)

    # 3. Assert: Comprobamos si las claves 'username' y 'role' existen
    #    en el payload del token y si tienen los valores correctos.
    assert 'username' in token
    assert token['username'] == 'test_admin'
    assert 'role' in token
    assert token['role'] == 'ADMIN'

# --- (Aquí añadiremos más pruebas después) ---
# backend/users/tests.py
# ... (imports existentes) ...
from django.urls import reverse # <-- Añade este import

# ... (todas tus pruebas unitarias U-B-001, 002, 004)...

# --- PRUEBAS DE INTEGRACIÓN (IL2) ---

@pytest.mark.django_db
def test_integration_I001_successful_login(client):
    """
    PRUEBA DE INTEGRACIÓN I-001: Flujo de Autenticación Exitosa.
    Verifica que la API /api/users/login/ responda correctamente.

    El 'client' es un navegador simulado que nos da pytest-django.
    """
    # 1. Arrange: 
    #    Creamos el usuario 'admin' con la contraseña que conocemos
    #    y le asignamos su rol ADMIN.
    user = User.objects.create_user(username='admin', password='CHOcho2002')
    profile = Profile.objects.get(user=user)
    profile.role = 'ADMIN'
    profile.save()

    # Obtenemos la URL de login (en lugar de escribirla a mano)
    url = reverse('token_obtain_pair') # Este 'name' lo pusimos en users/urls.py

    # Datos que el frontend enviaría
    data = {
        'username': 'admin',
        'password': 'CHOcho2002'
    }

    # 2. Act: 
    #    Usamos el 'client' para simular un POST a la URL con los datos.
    #    Le pedimos que formatee los datos como 'json'.
    response = client.post(url, data, content_type='application/json')

    # 3. Assert: 
    #    Verificamos que el Backend respondió correctamente.

    # 3.1: ¿El código de estado fue 200 OK?
    assert response.status_code == 200

    # 3.2: ¿La respuesta (el token) contiene la clave 'access'?
    assert 'access' in response.data

    # 3.3: ¿El token decodificado contiene el rol 'ADMIN'?
    # (Esto es casi igual a nuestra prueba unitaria U-B-004,
    # pero ahora probamos que la API *completa* lo devuelva)
    from jwt import decode
    from django.conf import settings

    # Decodificamos el token (sin verificar la firma, solo para leerlo)
    token_payload = decode(response.data['access'], options={"verify_signature": False})

    assert token_payload['role'] == 'ADMIN'
    assert token_payload['username'] == 'admin'


# ... (imports existentes) ...
from django.urls import reverse
from jwt import decode
from django.conf import settings

# ... (todas tus pruebas unitarias U-B-001, 002, 004)...

# ... (Prueba de Integración I-001 que ya hicimos)...
@pytest.mark.django_db
def test_integration_I001_successful_login(client):
    # ... (código existente) ...
    user = User.objects.create_user(username='admin', password='CHOcho2002')
    profile = Profile.objects.get(user=user)
    profile.role = 'ADMIN'
    profile.save()
    url = reverse('token_obtain_pair')
    data = {'username': 'admin', 'password': 'CHOcho2002'}
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 200
    assert 'access' in response.data

# --- ¡NUEVA PRUEBA DE INTEGRACIÓN I-002! ---
@pytest.mark.django_db
def test_integration_I002_failed_login_wrong_password(client):
    """
    PRUEBA DE INTEGRACIÓN I-002: Flujo de Autenticación Fallida.
    Verifica que la API /api/users/login/ rechace credenciales incorrectas.
    """
    # 1. Arrange: 
    #    Creamos el usuario 'admin' con la contraseña correcta
    #    para asegurarnos de que el usuario SÍ existe.
    User.objects.create_user(username='admin', password='CHOcho2002')

    # Obtenemos la URL de login
    url = reverse('token_obtain_pair')

    # Datos que el frontend enviaría, PERO con la contraseña mal
    data = {
        'username': 'admin',
        'password': 'password_incorrecto'
    }

    # 2. Act: 
    #    Simulamos el POST con los datos incorrectos.
    response = client.post(url, data, content_type='application/json')

    # 3. Assert: 
    #    Verificamos que el Backend nos rechazó correctamente.

    # 3.1: ¿El código de estado fue 401 Unauthorized?
    assert response.status_code == 401

    # 3.2: ¿La respuesta (el token) NO contiene la clave 'access'?
    assert 'access' not in response.data

    # 3.3: ¿La respuesta contiene un 'detail' de error? (Opcional pero bueno)
    assert 'detail' in response.data