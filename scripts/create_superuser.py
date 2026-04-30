"""
Script para criar superusuário automaticamente em ambiente de desenvolvimento.
Uso: docker-compose exec web python scripts/create_superuser.py
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from apps.accounts.infrastructure.models import User

username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@rh.local")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name="Administrador",
        role=User.Role.ADMIN,
    )
    print(f"Superusuario criado: {username} / {password}")
else:
    print(f"Superusuario '{username}' ja existe.")