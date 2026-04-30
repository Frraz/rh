from django.db import models
from simple_history.models import HistoricalRecords
from core.infrastructure.models.base import BaseModel, ActiveManager, AllObjectsManager


class DocumentType(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(blank=True, verbose_name="Descrição")
    has_expiry = models.BooleanField(default=True, verbose_name="Tem validade?")
    alert_days_before = models.PositiveIntegerField(default=30, verbose_name="Alertar dias antes")
    is_required = models.BooleanField(default=False, verbose_name="Obrigatório")

    objects = ActiveManager()
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Tipo de documento"
        verbose_name_plural = "Tipos de documentos"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Document(BaseModel):
    class Status(models.TextChoices):
        VALID = "valid", "Válido"
        EXPIRING = "expiring", "Vencendo"
        EXPIRED = "expired", "Vencido"

    person = models.ForeignKey(
        "employees.Person", on_delete=models.PROTECT, related_name="documents", verbose_name="Colaborador"
    )
    document_type = models.ForeignKey(
        DocumentType, on_delete=models.PROTECT, related_name="documents", verbose_name="Tipo"
    )
    file = models.FileField(upload_to="documents/%Y/%m/", verbose_name="Arquivo")
    issue_date = models.DateField(null=True, blank=True, verbose_name="Data de emissão")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="Data de vencimento")
    number = models.CharField(max_length=50, blank=True, verbose_name="Número")
    notes = models.TextField(blank=True, verbose_name="Observações")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.VALID, verbose_name="Status")

    objects = ActiveManager()
    all_objects = AllObjectsManager()
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.document_type.name} - {self.person.name}"
