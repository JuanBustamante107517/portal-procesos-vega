# backend/users/management/commands/changepassword.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Cambia la contraseña de un usuario'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario')
        parser.add_argument('new_password', type=str, help='Nueva contraseña')

    def handle(self, *args, **options):
        username = options['username']
        new_password = options['new_password']

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Contraseña actualizada exitosamente para el usuario: {username}\n'
                )
            )

        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ El usuario "{username}" no existe.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error al cambiar contraseña: {str(e)}')
            )

