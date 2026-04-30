from django.db import models
from simple_history.models import HistoricalRecords
from core.infrastructure.models.base import BaseModel, ActiveManager, AllObjectsManager


class Entity(BaseModel):
    name = models.CharField(max_length=200, verbose_name="Nome")
    cnpj = models.CharField(max_length=18, blank=True, verbose_name="CNPJ")
    address = models.TextField(blank=True, verbose_name="Endereço")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    is_active = models.BooleanField(default=True, verbose_name="Ativa")

    objects = ActiveManager()
    all_objects = AllObjectsManager()
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Entidade"
        verbose_name_plural = "Entidades"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Farm(BaseModel):
    entity = models.ForeignKey(
        Entity, on_delete=models.PROTECT, related_name="farms", verbose_name="Entidade"
    )
    name = models.CharField(max_length=200, verbose_name="Nome")
    city = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    state = models.CharField(max_length=2, blank=True, verbose_name="UF")
    is_active = models.BooleanField(default=True, verbose_name="Ativa")

    objects = ActiveManager()
    all_objects = AllObjectsManager()
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Fazenda"
        verbose_name_plural = "Fazendas"
        ordering = ["entity", "name"]

    def __str__(self):
        return f"{self.name} ({self.entity.name})"


class JobRole(BaseModel):
    entity = models.ForeignKey(
        Entity, on_delete=models.PROTECT, related_name="job_roles", verbose_name="Entidade"
    )
    name = models.CharField(max_length=100, verbose_name="Nome do Cargo")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    objects = ActiveManager()
    all_objects = AllObjectsManager()
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Função"
        verbose_name_plural = "Funções"
        ordering = ["entity", "name"]
        unique_together = [["entity", "name"]]

    def __str__(self):
        return self.name


class Person(BaseModel):
    class PersonType(models.TextChoices):
        EMPLOYEE = "employee", "Funcionário CLT"
        DAILY = "daily", "Diarista"

    class Status(models.TextChoices):
        ACTIVE = "active", "Ativo"
        INACTIVE = "inactive", "Inativo"

    class MaritalStatus(models.TextChoices):
        SINGLE = "single", "Solteiro(a)"
        MARRIED = "married", "Casado(a)"
        DIVORCED = "divorced", "Divorciado(a)"
        WIDOWED = "widowed", "Viúvo(a)"
        OTHER = "other", "Outro"

    entity = models.ForeignKey(Entity, on_delete=models.PROTECT, related_name="persons", verbose_name="Entidade")
    farm = models.ForeignKey(Farm, on_delete=models.PROTECT, related_name="persons", verbose_name="Fazenda")
    job_role = models.ForeignKey(JobRole, on_delete=models.PROTECT, related_name="persons", verbose_name="Função")
    person_type = models.CharField(max_length=10, choices=PersonType.choices, verbose_name="Tipo")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE, verbose_name="Status")
    name = models.CharField(max_length=200, verbose_name="Nome completo")
    cpf = models.CharField(max_length=14, verbose_name="CPF")
    rg = models.CharField(max_length=20, blank=True, verbose_name="RG")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Data de nascimento")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    address = models.TextField(blank=True, verbose_name="Endereço")
    marital_status = models.CharField(max_length=10, choices=MaritalStatus.choices, blank=True, verbose_name="Estado civil")
    photo = models.ImageField(upload_to="photos/", null=True, blank=True, verbose_name="Foto")
    admission_date = models.DateField(verbose_name="Data de admissão")
    termination_date = models.DateField(null=True, blank=True, verbose_name="Data de demissão")
    pis = models.CharField(max_length=20, blank=True, verbose_name="PIS/PASEP")
    ctps = models.CharField(max_length=20, blank=True, verbose_name="CTPS")
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Salário (CLT)")
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor da diária")
    bank = models.CharField(max_length=100, blank=True, verbose_name="Banco")
    bank_agency = models.CharField(max_length=20, blank=True, verbose_name="Agência")
    bank_account = models.CharField(max_length=30, blank=True, verbose_name="Conta")
    notes = models.TextField(blank=True, verbose_name="Observações")

    objects = ActiveManager()
    all_objects = AllObjectsManager()
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["entity", "status"]),
            models.Index(fields=["person_type", "status"]),
            models.Index(fields=["cpf"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_person_type_display()})"

    @property
    def is_employee(self):
        return self.person_type == self.PersonType.EMPLOYEE

    @property
    def is_daily_worker(self):
        return self.person_type == self.PersonType.DAILY

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE
