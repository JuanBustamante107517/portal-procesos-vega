# backend/users/management/commands/createuser.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile


class Command(BaseCommand):
    help = 'Crea un usuario con perfil y rol específico'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario')
        parser.add_argument('email', type=str, help='Email del usuario')
        parser.add_argument('password', type=str, help='Contraseña del usuario')
        parser.add_argument(
            '--role',
            type=str,
            default='CAJERO',
            choices=['ADMIN', 'JEFE', 'CAJERO'],
            help='Rol del usuario (ADMIN, JEFE, CAJERO). Por defecto: CAJERO'
        )
        parser.add_argument(
            '--first-name',
            type=str,
            default='',
            help='Nombre del usuario'
        )
        parser.add_argument(
            '--last-name',
            type=str,
            default='',
            help='Apellido del usuario'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        role = options['role']
        first_name = options.get('first_name', '')
        last_name = options.get('last_name', '')

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.ERROR(f'❌ El usuario "{username}" ya existe.')
            )
            return

        # Verificar si el email ya existe
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f'❌ El email "{email}" ya está en uso.')
            )
            return

        try:
            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # El perfil se crea automáticamente por la señal (signal)
            # pero vamos a asignar el rol explícitamente
            profile = user.profile
            profile.role = role
            profile.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Usuario creado exitosamente:\n'
                    f'   👤 Username: {username}\n'
                    f'   📧 Email: {email}\n'
                    f'   🎭 Rol: {profile.get_role_display()}\n'
                    f'   📝 Nombre completo: {first_name} {last_name}\n'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error al crear usuario: {str(e)}')
            )

