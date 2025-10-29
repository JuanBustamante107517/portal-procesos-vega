# backend/users/models.py

from django.db import models
from django.contrib.auth.models import User

# Estos son los "Roles" que definimos.
# Son fijos y no se pueden cambiar fácilmente.
class Profile(models.Model):

    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'), # Puede crear/editar/borrar todo
        ('JEFE', 'Jefe'),             # Puede descargar
        ('CAJERO', 'Cajero'),           # Puede descargar
    )

    # Conectamos este Perfil con el Usuario de Django (uno-a-uno)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Este es el campo clave: el 'rol' del usuario.
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CAJERO')

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"