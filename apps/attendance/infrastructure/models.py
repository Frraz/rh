from django.db import models
from simple_history.models import HistoricalRecords

from core.infrastructure.models.base import ActiveManager, AllObjectsManager, BaseModel


class DiscountInstallment(BaseModel):
    """
    Desconto parcelado. Representa um desconto que será aplicado
    em múltiplos meses de referência.
    Exemplo: adiantamento de R$5.000 em 5x R$1.000.
    Cada parcela gera um Adjustment individual por mês.
    """

    class InstallmentType(models.TextChoices):
        ADVANCE = "advance", "Adiantamento"
        LOAN = "loan", "Empréstimo"
        OTHER = "other", "Outro desconto parcelado"

    person = models.ForeignKey(
        "employees.Person",
        on_delete=models.PROTECT,
        related_name="installments",
        verbose_name="Colaborador",
    )
    installment_type = models.CharField(
        max_length=20,
        choices=InstallmentType.choices,
        verbose_name="Tipo",
    )
    description = models.CharField(max_length=200, verbose_name="Descrição")
    total_value = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor total"
    )
    num_installments = models.PositiveSmallIntegerField(
        verbose_name="Número de parcelas"
    )
    installment_value = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor por parcela"
    )
    first_reference_year = models.PositiveSmallIntegerField(verbose_name="Ano inicial")
    first_reference_month = models.PositiveSmallIntegerField(verbose_name="Mês inicial")
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="installments_created",
        verbose_name="Criado por",
    )

    objects = ActiveManager()
    all_objects = AllObjectsManager()
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Desconto parcelado"
        verbose_name_plural = "Descontos parcelados"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.person.name} | {self.description} | {self.num_installments}x R${self.installment_value}"


class Adjustment(BaseModel):
    """
    Ajuste financeiro individual vinculado a um mês de referência.
    Pode ser criado manualmente ou gerado automaticamente por um DiscountInstallment.
    Valor negativo = desconto. Valor positivo = crédito.
    """

    class AdjustmentType(models.TextChoices):
        ABSENCE = "absence", "Falta"
        ADVANCE = "advance", "Adiantamento"
        INSTALLMENT = "installment", "Parcela de desconto"
        FINE = "fine", "Multa"
        TRANSPORT = "transport", "Vale transporte"
        HEALTH = "health", "Plano de saúde"
        OTHER_DISCOUNT = "other_discount", "Outro desconto"
        OVERTIME = "overtime", "Hora extra"
        BONUS = "bonus", "Bônus / Gratificação"
        OTHER_CREDIT = "other_credit", "Outro crédito"

    class Origin(models.TextChoices):
        MANUAL = "manual", "Manual"
        SYSTEM = "system", "Sistema"
        INSTALLMENT_MODULE = "installment_module", "Módulo de parcelamento"
        ADVANCE_MODULE = "advance_module", "Módulo de adiantamentos"

    person = models.ForeignKey(
        "employees.Person",
        on_delete=models.PROTECT,
        related_name="adjustments",
        verbose_name="Colaborador",
    )
    adjustment_type = models.CharField(
        max_length=20,
        choices=AdjustmentType.choices,
        verbose_name="Tipo",
    )
    reference_year = models.PositiveSmallIntegerField(verbose_name="Ano de referência")
    reference_month = models.PositiveSmallIntegerField(verbose_name="Mês de referência")
    event_date = models.DateField(verbose_name="Data do evento")
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor",
        help_text="Negativo para desconto, positivo para crédito.",
    )
    origin = models.CharField(
        max_length=20,
        choices=Origin.choices,
        default=Origin.MANUAL,
        verbose_name="Origem",
    )
    description = models.TextField(verbose_name="Descrição")
    installment = models.ForeignKey(
        DiscountInstallment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="adjustments",
        verbose_name="Parcelamento origem",
    )
    installment_number = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Número da parcela",
    )
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="adjustments_created",
        verbose_name="Criado por",
    )

    objects = ActiveManager()
    all_objects = AllObjectsManager()
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Ajuste"
        verbose_name_plural = "Ajustes"
        ordering = ["-reference_year", "-reference_month", "person__name"]
        indexes = [
            models.Index(fields=["person", "reference_year", "reference_month"]),
            models.Index(
                fields=["adjustment_type", "reference_year", "reference_month"]
            ),
        ]

    def __str__(self):
        return (
            f"{self.person.name} | {self.get_adjustment_type_display()} | "
            f"{self.reference_month:02d}/{self.reference_year} | R${self.value}"
        )

    @property
    def is_discount(self):
        return self.value < 0
