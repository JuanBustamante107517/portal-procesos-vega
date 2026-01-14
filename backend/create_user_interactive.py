#!/usr/bin/env python
"""
Script para crear usuarios de forma interactiva en el Portal de Procesos Vega
Ejecutar desde el directorio backend con: python create_user_interactive.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from users.models import Profile


def get_input(prompt, default=None):
    """Obtiene input del usuario con valor por defecto opcional"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "

    value = input(prompt).strip()
    return value if value else default


def validate_role(role):
    """Valida que el rol sea válido"""
    valid_roles = ['ADMIN', 'JEFE', 'CAJERO']
    return role.upper() in valid_roles


def create_user_interactive():
    """Crea un usuario de forma interactiva"""
    print("\n" + "="*60)
    print("🚀 CREADOR DE USUARIOS - Portal de Procesos Vega")
    print("="*60 + "\n")

    # Obtener datos del usuario
    username = get_input("👤 Username (obligatorio)")
    if not username:
        print("❌ El username es obligatorio.")
        return

    # Verificar si existe
    if User.objects.filter(username=username).exists():
        print(f"❌ El usuario '{username}' ya existe.")
        return

    email = get_input("📧 Email (obligatorio)")
    if not email:
        print("❌ El email es obligatorio.")
        return

    # Verificar si el email existe
    if User.objects.filter(email=email).exists():
        print(f"❌ El email '{email}' ya está en uso.")
        return

    password = get_input("🔐 Contraseña (obligatorio)")
    if not password:
        print("❌ La contraseña es obligatoria.")
        return

    first_name = get_input("📝 Nombre", default="")
    last_name = get_input("📝 Apellido", default="")

    print("\n🎭 Roles disponibles:")
    print("   1. ADMIN - Administrador (acceso completo)")
    print("   2. JEFE - Jefe (puede consultar procesos)")
    print("   3. CAJERO - Cajero (acceso limitado)")

    role_input = get_input("Seleccione rol (1-3)", default="3")

    role_map = {
        '1': 'ADMIN',
        '2': 'JEFE',
        '3': 'CAJERO'
    }

    role = role_map.get(role_input, 'CAJERO')

    # Confirmación
    print("\n" + "-"*60)
    print("📋 RESUMEN DEL USUARIO A CREAR:")
    print("-"*60)
    print(f"   👤 Username: {username}")
    print(f"   📧 Email: {email}")
    print(f"   🔐 Password: {'*' * len(password)}")
    print(f"   📝 Nombre: {first_name} {last_name}")
    print(f"   🎭 Rol: {role}")
    print("-"*60)

    confirm = get_input("\n¿Crear este usuario? (s/n)", default="s")

    if confirm.lower() not in ['s', 'si', 'yes', 'y']:
        print("❌ Operación cancelada.")
        return

    try:
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Asignar rol
        profile = user.profile
        profile.role = role
        profile.save()

        print("\n" + "="*60)
        print("✅ USUARIO CREADO EXITOSAMENTE")
        print("="*60)
        print(f"   👤 Username: {username}")
        print(f"   📧 Email: {email}")
        print(f"   🎭 Rol: {profile.get_role_display()}")
        print(f"   🆔 ID: {user.id}")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n❌ Error al crear usuario: {str(e)}\n")


if __name__ == "__main__":
    try:
        create_user_interactive()
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario.\n")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}\n")

