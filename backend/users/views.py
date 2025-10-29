# backend/users/views.py

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer # <-- Asegúrate que esta línea esté

# --- Vista de Login (Token) ---
class MyTokenObtainPairView(TokenObtainPairView): # <-- ¡Aquí está la clase!
    serializer_class = MyTokenObtainPairSerializer


# --- Vista de "Mi Perfil" (lo usaremos después) ---
from rest_framework import generics, permissions
from .serializers import UserSerializer

class MyProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user