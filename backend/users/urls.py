# backend/users/urls.py

from django.urls import path
from .views import MyTokenObtainPairView, MyProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # --- URLs de Autenticación ---

    # /api/users/login/ (Para Iniciar Sesión)
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # /api/users/refresh/ (Para refrescar el token)
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # /api/users/me/ (Para obtener datos del perfil)
    path('me/', MyProfileView.as_view(), name='my_profile'),

    # (Aquí pondremos /api/users/register/ y /api/users/password-reset/ después)
]