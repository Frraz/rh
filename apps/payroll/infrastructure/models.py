from django.db import models
from simple_history.models import HistoricalRecords
from core.infrastructure.models.base import BaseModel, ActiveManager


class Payroll(BaseModel):
    class Status(models.TextChoices):
        OPEN = "open", "Em aberto"
        CLOSED = "closed", "Fechada"

    entity = models.ForeignKey(
        "employees.Entity", on_delete=models.PROTECT, related_name="payrolls", verbose_name="Entidade"
    )
    reference_year = models.PositiveSmallIntegerField(verbose_name="Ano")
    reference_month = models.PositiveSmallIntegerField(verbose_name="Mês")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN, verbose_name="Status")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fechada em")
    closed_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="payrolls_closed", verbose_name="Fechada por"
    )
    notes = models.TextField(blank=True, verbose_name="Observações")

    objects = ActiveManager()
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Folha de pagamento"
        verbose_name_plural = "Folhas de pagamento"
        unique_together = [["entity", "reference_year", "reference_month"]]
        ordering = ["-reference_year", "-reference_month"]

    def __str__(self):
        return f"Folha {self.reference_month:02d}/{self.reference_year} - {self.entity.name}"


class PayrollItem(BaseModel):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name="items", verbose_name="Folha")
    person = models.ForeignKey(
        "employees.Person", on_delete=models.PROTECT, related_name="payroll_items", verbose_name="Colaborador"
    )
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salário bruto")
    worked_days = models.PositiveSmallIntegerField(default=30, verbose_name="Dias trabalhados")
    inss_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="INSS")
    advance_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Adiantamentos")
    absence_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Faltas")
    other_discounts = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Outros descontos")
    overtime_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Horas extras")
    other_credits = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Outros créditos")
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salário líquido")
    fgts_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="FGTS")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Item da folha"
        verbose_name_plural = "Itens da folha"
        unique_together = [["payroll", "person"]]

    def __str__(self):
        return f"{self.person.name} - {self.payroll}"


class Termination(BaseModel):
    class TerminationType(models.TextChoices):
        WITHOUT_CAUSE = "without_cause", "Demissão sem justa causa"
        WITH_CAUSE = "with_cause", "Demissão por justa causa"
        EMPLOYEE_REQUEST = "employee_request", "Pedido de demissão"
        MUTUAL_AGREEMENT = "mutual_agreement", "Acordo mútuo (art. 484-A)"
        OTHER = "other", "Outro"

    person = models.ForeignKey(
        "employees.Person", on_delete=models.PROTECT, related_name="terminations", verbose_name="Colaborador"
    )
    termination_type = models.CharField(max_length=20, choices=TerminationType.choices, verbose_name="Tipo de demissão")
    termination_date = models.DateField(verbose_name="Data de demissão")
    notice_date = models.DateField(null=True, blank=True, verbose_name="Data do aviso")
    notice_type = models.CharField(max_length=20, blank=True, verbose_name="Tipo de aviso")
    balance_days = models.PositiveSmallIntegerField(default=0, verbose_name="Dias de saldo")
    balance_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Saldo de salário")
    vacation_due_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Férias vencidas")
    vacation_prop_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Férias proporcionais")
    vacation_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="1/3 de férias")
    thirteenth_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="13º salário")
    fgts_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="FGTS a receber")
    fgts_fine = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Multa de 40% FGTS")
    gross_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total bruto")
    inss_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="INSS")
    net_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total líquido")
    calculation_memory = models.JSONField(default=dict, verbose_name="Memória de cálculo")
    notes = models.TextField(blank=True, verbose_name="Observações")
    calculated_by = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, null=True, blank=True,
        related_name="terminations_calculated", verbose_name="Calculado por"
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Rescisão"
        verbose_name_plural = "Rescisões"
        ordering = ["-termination_date"]

    def __str__(self):
        return f"Rescisão {self.person.name} - {self.termination_date}"
