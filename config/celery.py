import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("rh")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # Verificar documentos vencendo nos próximos 30 dias — diariamente às 08:00
    "check-expiring-documents": {
        "task": "apps.documents.infrastructure.tasks.check_expiring_documents",
        "schedule": crontab(hour=8, minute=0),
    },
}