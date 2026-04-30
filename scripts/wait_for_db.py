"""
Script para aguardar o banco de dados estar disponível.
Usado pelo Docker Compose antes de iniciar o Django.
"""
import time
import sys
import os
import django
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()


def wait_for_db(max_retries: int = 30, delay: float = 2.0):
    print("Aguardando banco de dados...")
    for attempt in range(1, max_retries + 1):
        try:
            conn = connections["default"]
            conn.ensure_connection()
            print(f"Banco de dados disponivel apos {attempt} tentativa(s).")
            return True
        except OperationalError:
            print(f"Tentativa {attempt}/{max_retries} — aguardando {delay}s...")
            time.sleep(delay)
    print("ERRO: banco de dados nao ficou disponivel a tempo.")
    sys.exit(1)


if __name__ == "__main__":
    wait_for_db()