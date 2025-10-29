# backend/users/serializers.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

# --- Serializador de Usuario (para ver datos) ---
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True) # <-- Lo ponemos read_only

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


# --- Serializador de Token (EL IMPORTANTE) ---
# Personalizamos el token para que incluya el ROL
# ... (UserSerializer y ProfileSerializer sin cambios arriba) ...

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user) # Obtiene el token base

        # --- Añadimos nuestros datos personalizados ---
        token['username'] = user.username

        # --- CORRECCIÓN AQUÍ ---
        # En lugar de confiar en user.profile (que podría estar desactualizado),
        # volvemos a buscar el perfil desde la base de datos para asegurarnos
        # de tener el valor más reciente del rol.
        try:
            profile = Profile.objects.get(user=user) # Buscamos de nuevo
            token['role'] = profile.role
        except Profile.DoesNotExist: # Manejo por si el perfil no existe (poco probable)
            token['role'] = None
        # --- FIN DE LA CORRECCIÓN ---

        return token