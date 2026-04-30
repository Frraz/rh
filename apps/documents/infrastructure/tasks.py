"""Tarefas assíncronas do módulo de documentos."""
import logging
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


@shared_task(name="apps.documents.infrastructure.tasks.check_expiring_documents")
def check_expiring_documents():
    """
    Verifica documentos vencendo nos próximos dias e atualiza seus status.
    Executado diariamente pelo Celery Beat.
    """
    from .models import Document

    today = timezone.now().date()

    # Marca como vencido
    expired_count = Document.objects.filter(
        expiry_date__lt=today,
        status__in=["valid", "expiring"],
        is_deleted=False,
    ).update(status="expired")

    # Marca como vencendo
    alert_window = today + timedelta(days=30)
    expiring_count = Document.objects.filter(
        expiry_date__gte=today,
        expiry_date__lte=alert_window,
        status="valid",
        is_deleted=False,
    ).update(status="expiring")

    logger.info(
        "Documentos verificados: %s vencidos, %s vencendo",
        expired_count,
        expiring_count,
    )
    return {"expired": expired_count, "expiring": expiring_count}