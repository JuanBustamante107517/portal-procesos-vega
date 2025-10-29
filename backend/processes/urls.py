# backend/processes/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProcesoViewSet

router = DefaultRouter()
router.register(r'', ProcesoViewSet, basename='proceso')

urlpatterns = [
    path('', include(router.urls)),
]