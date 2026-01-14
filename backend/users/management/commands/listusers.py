# backend/users/management/commands/listusers.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile


class Command(BaseCommand):
    help = 'Lista todos los usuarios del sistema con sus roles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--role',
            type=str,
            choices=['ADMIN', 'JEFE', 'CAJERO'],
            help='Filtrar usuarios por rol específico'
        )

    def handle(self, *args, **options):
        role_filter = options.get('role')

        users = User.objects.all().select_related('profile')

        if role_filter:
            users = users.filter(profile__role=role_filter)

        if not users.exists():
            self.stdout.write(
                self.style.WARNING('⚠️  No se encontraron usuarios.')
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'\n📋 Lista de usuarios ({users.count()} encontrados):\n')
        )
        self.stdout.write('=' * 100)

        for user in users:
            try:
                profile = user.profile
                role_display = profile.get_role_display()
                role_emoji = {
                    'ADMIN': '👑',
                    'JEFE': '📊',
                    'CAJERO': '💰'
                }.get(profile.role, '👤')

                self.stdout.write(
                    f'\n{role_emoji} ID: {user.id:<4} | Username: {user.username:<20} | '
                    f'Email: {user.email:<30} | '
                    f'Rol: {role_display:<15} | '
                    f'Activo: {"✅" if user.is_active else "❌"}'
                )
                if user.first_name or user.last_name:
                    self.stdout.write(f'   Nombre: {user.first_name} {user.last_name}')
            except Profile.DoesNotExist:
                self.stdout.write(
                    f'\n⚠️  ID: {user.id:<4} | Username: {user.username:<20} | '
                    f'SIN PERFIL'
                )

        self.stdout.write('\n' + '=' * 100 + '\n')

