from django.db import models
from simple_history.models import HistoricalRecords
from core.infrastructure.models.base import BaseModel, ActiveManager, AllObjectsManager


class Advance(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendente"
        APPROVED = "approved", "Aprovado"
        REJECTED = "rejected", "Rejeitado"
        DISCOUNTED = "discounted", "Descontado"

    person = models.ForeignKey(
        "employees.Person", on_delete=models.PROTECT, related_name="advances", verbose_name="Colaborador"
    )
    requested_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor solicitado")
    approved_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor aprovado")
    request_date = models.DateField(verbose_name="Data da solicitação")
    discount_reference_year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Ano de desconto")
    discount_reference_month = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Mês de desconto")
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING, verbose_name="Status")
    reason = models.TextField(blank=True, verbose_name="Motivo")
    rejection_reason = models.TextField(blank=True, verbose_name="Motivo de rejeição")
    requested_by = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, related_name="advances_requested", verbose_name="Solicitado por"
    )
    reviewed_by = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, null=True, blank=True,
        related_name="advances_reviewed", verbose_name="Avaliado por"
    )
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name="Avaliado em")
    generated_adjustment = models.OneToOneField(
        "attendance.Adjustment", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="advance", verbose_name="Ajuste gerado"
    )

    objects = ActiveManager()
    all_objects = AllObjectsManager()
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Adiantamento"
        verbose_name_plural = "Adiantamentos"
        ordering = ["-request_date"]

    def __str__(self):
        return f"{self.person.name} | R$ {self.requested_value} | {self.get_status_display()}"
