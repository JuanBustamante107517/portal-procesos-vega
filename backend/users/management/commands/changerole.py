# backend/users/management/commands/changerole.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile


class Command(BaseCommand):
    help = 'Cambia el rol de un usuario existente'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario')
        parser.add_argument(
            'role',
            type=str,
            choices=['ADMIN', 'JEFE', 'CAJERO'],
            help='Nuevo rol (ADMIN, JEFE, CAJERO)'
        )

    def handle(self, *args, **options):
        username = options['username']
        new_role = options['role']

        try:
            user = User.objects.get(username=username)
            profile = user.profile
            old_role = profile.get_role_display()

            profile.role = new_role
            profile.save()

            new_role_display = profile.get_role_display()

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Rol actualizado exitosamente:\n'
                    f'   👤 Usuario: {username}\n'
                    f'   🔄 Rol anterior: {old_role}\n'
                    f'   🎭 Rol nuevo: {new_role_display}\n'
                )
            )

        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ El usuario "{username}" no existe.')
            )
        except Profile.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ El usuario "{username}" no tiene perfil asociado.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error al cambiar rol: {str(e)}')
            )

