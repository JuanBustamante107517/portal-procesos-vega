"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# backend/core/urls.py
from django.contrib import admin
from django.urls import path, include
# Importa las vistas de SimpleJWT (Seguridad)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 1. Panel de Admin
    path('admin/', admin.site.urls),

    # 2. Rutas de tu Aplicación (Lo que ya tenías)
    path('api/users/', include('users.urls')),
    path('api/processes/', include('processes.urls')),

    # 3. Rutas para el Login (¡ESTO ES LO NUEVO QUE NECESITAS!)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # El Login real
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Para refrescar sesión
]
