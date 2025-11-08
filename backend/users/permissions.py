# backend/users/permissions.py
from rest_framework import permissions

class IsAdminOrJefe(permissions.BasePermission):
    """
    Permiso personalizado para permitir acceso solo a ADMIN o JEFE.
    """
    def has_permission(self, request, view):
        # 1. ¿Está logueado?
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. ¿Tiene perfil y rol?
        try:
            role = request.user.profile.role
        except:
            return False # No tiene perfil, denegar

        # 3. ¿El rol es ADMIN o JEFE?
        return role in ('ADMIN', 'JEFE')