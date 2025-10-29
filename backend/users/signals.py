# backend/users/signals.py

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# Esta función se ejecutará CADA VEZ que un 'User' sea guardado.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Crea un perfil de usuario automáticamente cuando se crea un usuario.
    Actualiza el perfil cuando se actualiza el usuario.
    """
    if created:
        # Si el usuario es nuevo, crea su perfil.
        Profile.objects.create(user=instance)

    # Guarda el perfil (esto es útil si el 'User' se actualiza)
    instance.profile.save()