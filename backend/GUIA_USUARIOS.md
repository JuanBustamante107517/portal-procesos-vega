# Guía de Gestión de Usuarios - Portal de Procesos Vega

## 📚 Índice
1. [Métodos para Crear Usuarios](#métodos-para-crear-usuarios)
2. [Comandos de Gestión](#comandos-de-gestión)
3. [Uso del Shell de Django](#uso-del-shell-de-django)
4. [Ejemplos Prácticos](#ejemplos-prácticos)
5. [Solución de Problemas](#solución-de-problemas)

---

## 🎯 Métodos para Crear Usuarios

### Método 1: Script Interactivo (Más Fácil) ⭐

```bash
# Desde el directorio backend/
python create_user_interactive.py
```

El script te guiará paso a paso para crear un usuario. Es la forma más sencilla.

---

### Método 2: Comando de Gestión Django

#### 2.1 Crear Usuario

```bash
# Sintaxis básica (crea un CAJERO por defecto)
python manage.py createuser <username> <email> <password>

# Ejemplo básico
python manage.py createuser juan juan@empresa.com MiPassword123

# Con rol específico
python manage.py createuser admin admin@empresa.com Admin123 --role ADMIN

# Con nombre completo
python manage.py createuser maria maria@empresa.com Maria456 --role JEFE --first-name María --last-name González
```

**Opciones disponibles:**
- `--role`: ADMIN, JEFE, o CAJERO (por defecto: CAJERO)
- `--first-name`: Nombre del usuario
- `--last-name`: Apellido del usuario

#### 2.2 Listar Usuarios

```bash
# Listar todos los usuarios
python manage.py listusers

# Filtrar por rol
python manage.py listusers --role ADMIN
python manage.py listusers --role JEFE
python manage.py listusers --role CAJERO
```

#### 2.3 Cambiar Contraseña

```bash
python manage.py changepassword <username> <nueva_contraseña>

# Ejemplo
python manage.py changepassword juan NuevaPassword456
```

#### 2.4 Cambiar Rol

```bash
python manage.py changerole <username> <nuevo_rol>

# Ejemplos
python manage.py changerole juan ADMIN
python manage.py changerole maria JEFE
python manage.py changerole pedro CAJERO
```

---

### Método 3: Shell de Django (Para Usuarios Avanzados)

```bash
python manage.py shell
```

Luego ejecuta estos comandos:

```python
from django.contrib.auth.models import User
from users.models import Profile

# Crear usuario básico
user = User.objects.create_user(
    username='nuevo_usuario',
    email='usuario@email.com',
    password='password123',
    first_name='Nombre',
    last_name='Apellido'
)

# Asignar rol (el perfil se crea automáticamente)
user.profile.role = 'ADMIN'  # o 'JEFE' o 'CAJERO'
user.profile.save()

print(f"Usuario creado: {user.username} con rol {user.profile.get_role_display()}")
```

---

### Método 4: Usar Docker Compose

Si tu aplicación está en Docker:

```bash
# Acceder al contenedor
docker-compose exec backend bash

# Luego usa cualquiera de los métodos anteriores
python manage.py createuser admin admin@empresa.com Admin123 --role ADMIN
```

---

## 📋 Ejemplos Prácticos

### Crear Usuarios de Prueba

```bash
# 1. Crear un Administrador
python manage.py createuser admin admin@vega.com Admin123! --role ADMIN --first-name Admin --last-name Sistema

# 2. Crear un Jefe
python manage.py createuser jefe1 jefe@vega.com Jefe123! --role JEFE --first-name Carlos --last-name Rodríguez

# 3. Crear un Cajero
python manage.py createuser cajero1 cajero@vega.com Cajero123! --role CAJERO --first-name Ana --last-name Martínez

# 4. Listar todos los usuarios creados
python manage.py listusers
```

### Gestionar Usuarios Existentes

```bash
# Ver usuarios ADMIN
python manage.py listusers --role ADMIN

# Cambiar contraseña de un usuario
python manage.py changepassword cajero1 NuevaPassword456

# Promover un usuario a JEFE
python manage.py changerole cajero1 JEFE

# Degradar un ADMIN a CAJERO
python manage.py changerole admin CAJERO
```

---

## 🏗️ Estructura de Roles

### ADMIN (Administrador) 👑
- Acceso completo al sistema
- Puede crear, editar y eliminar procesos
- Puede gestionar usuarios
- Puede ver todos los procesos (B2B y B2C)

### JEFE 📊
- Puede consultar procesos
- Puede filtrar por tipo de venta
- Puede descargar información
- NO puede modificar procesos

### CAJERO 💰
- Acceso limitado
- NO puede ver procesos
- Puede realizar operaciones básicas

---

## 🔐 Seguridad

### Buenas Prácticas para Contraseñas

```bash
# ❌ Contraseñas débiles (EVITAR)
python manage.py createuser user user@email.com 123

# ✅ Contraseñas fuertes (USAR)
python manage.py createuser user user@email.com MyP@ssw0rd2024!
```

**Recomendaciones:**
- Mínimo 8 caracteres
- Combinar mayúsculas, minúsculas, números y símbolos
- No usar información personal
- Cambiar contraseñas periódicamente

---

## 🐍 Crear Usuarios con Python (Programáticamente)

Crea un archivo `create_users.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile

def create_user(username, email, password, role='CAJERO', first_name='', last_name=''):
    """Función para crear usuarios"""
    try:
        if User.objects.filter(username=username).exists():
            print(f"❌ Usuario {username} ya existe")
            return None
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        user.profile.role = role
        user.profile.save()
        
        print(f"✅ Usuario {username} creado con rol {role}")
        return user
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Crear usuarios de ejemplo
users = [
    ('admin', 'admin@vega.com', 'Admin123!', 'ADMIN', 'Admin', 'Sistema'),
    ('jefe1', 'jefe1@vega.com', 'Jefe123!', 'JEFE', 'Carlos', 'Rodríguez'),
    ('jefe2', 'jefe2@vega.com', 'Jefe456!', 'JEFE', 'María', 'López'),
    ('cajero1', 'cajero1@vega.com', 'Cajero123!', 'CAJERO', 'Ana', 'Martínez'),
    ('cajero2', 'cajero2@vega.com', 'Cajero456!', 'CAJERO', 'Pedro', 'García'),
]

for username, email, password, role, first_name, last_name in users:
    create_user(username, email, password, role, first_name, last_name)

print("\n✅ Proceso completado")
```

Ejecutar:
```bash
python create_users.py
```

---

## 🔍 Verificar Usuarios Creados

### Desde la Terminal

```bash
# Listar todos
python manage.py listusers

# Solo ADMIN
python manage.py listusers --role ADMIN

# Verificar en el shell
python manage.py shell
```

En el shell:
```python
from django.contrib.auth.models import User

# Ver todos los usuarios
for user in User.objects.all():
    print(f"{user.username} - {user.profile.role}")

# Ver usuarios por rol
admins = User.objects.filter(profile__role='ADMIN')
print(f"Total ADMIN: {admins.count()}")
```

---

## 🚨 Solución de Problemas

### Error: "Profile matching query does not exist"

**Solución:**
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from users.models import Profile

# Crear perfiles faltantes
for user in User.objects.all():
    Profile.objects.get_or_create(user=user)
```

### Error: "Username already exists"

El usuario ya existe. Opciones:
1. Usar otro username
2. Eliminar el usuario existente (cuidado en producción)

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
User.objects.get(username='nombre_usuario').delete()
```

### Error: "Permission denied"

Asegúrate de estar en el entorno correcto:

```bash
# Activar entorno virtual (si aplica)
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# O usar Docker
docker-compose exec backend python manage.py createuser ...
```

---

## 📞 Comandos Rápidos de Referencia

```bash
# Crear usuario básico
python manage.py createuser username email@test.com password123

# Crear ADMIN
python manage.py createuser admin admin@test.com admin123 --role ADMIN

# Listar usuarios
python manage.py listusers

# Cambiar contraseña
python manage.py changepassword username newpass123

# Cambiar rol
python manage.py changerole username JEFE

# Script interactivo
python create_user_interactive.py
```

---

## 🎓 Roles y Permisos

| Acción | ADMIN | JEFE | CAJERO |
|--------|-------|------|--------|
| Ver procesos | ✅ | ✅ | ❌ |
| Filtrar por tipo_venta | ✅ | ✅ | ❌ |
| Crear procesos | ✅ | ❌ | ❌ |
| Editar procesos | ✅ | ❌ | ❌ |
| Eliminar procesos | ✅ | ❌ | ❌ |
| Gestionar usuarios | ✅ | ❌ | ❌ |

---

## 📝 Notas Adicionales

1. **Los perfiles se crean automáticamente** cuando creas un usuario gracias a las señales de Django
2. **El rol por defecto es CAJERO** si no especificas otro
3. **Las contraseñas se encriptan automáticamente** con Django
4. **Los tokens JWT incluyen el rol del usuario** para autorización

---

## 🔗 Enlaces Útiles

- Documentación Django Users: https://docs.djangoproject.com/en/stable/topics/auth/
- Django REST Framework: https://www.django-rest-framework.org/
- Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/

---

**Última actualización:** 2026-01-13
**Versión:** 1.0.0

