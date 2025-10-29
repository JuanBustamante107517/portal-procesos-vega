# backend/users/tests.py
import pytest
from django.contrib.auth.models import User
from users.models import Profile # Asegúrate que Profile esté importado
# ¡Importamos nuestro serializador de token personalizado!
from users.serializers import MyTokenObtainPairSerializer

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