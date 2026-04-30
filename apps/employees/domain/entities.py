"""Entidades de domínio do módulo de funcionários."""
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional


class PersonType(str, Enum):
    EMPLOYEE = "employee"
    DAILY = "daily"

    @property
    def display(self):
        return {"employee": "Funcionário", "daily": "Diarista"}[self.value]


class PersonStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

    @property
    def display(self):
        return {"active": "Ativo", "inactive": "Inativo"}[self.value]


@dataclass
class EntityDomain:
    """Representa uma entidade (produtor/empresa)."""
    id: int
    name: str
    cnpj: Optional[str] = None
    is_active: bool = True


@dataclass
class FarmDomain:
    """Representa uma fazenda vinculada a uma entidade."""
    id: int
    name: str
    entity_id: int
    city: Optional[str] = None


@dataclass
class JobRoleDomain:
    """Representa uma função/cargo."""
    id: int
    name: str
    entity_id: int


@dataclass
class PersonDomain:
    """
    Representa um colaborador (funcionário CLT ou diarista).
    É a entidade central do domínio de RH.
    """
    id: int
    name: str
    cpf: str
    person_type: PersonType
    status: PersonStatus
    entity_id: int
    farm_id: int
    job_role_id: int
    admission_date: date
    salary: Decimal = Decimal("0.00")       # Para funcionários CLT
    daily_rate: Decimal = Decimal("0.00")   # Para diaristas
    phone: str = ""
    birth_date: Optional[date] = None
    pis: str = ""
    ctps: str = ""
    bank: str = ""
    bank_agency: str = ""
    bank_account: str = ""

    @property
    def is_employee(self) -> bool:
        return self.person_type == PersonType.EMPLOYEE

    @property
    def is_daily_worker(self) -> bool:
        return self.person_type == PersonType.DAILY

    @property
    def is_active(self) -> bool:
        return self.status == PersonStatus.ACTIVE

    def daily_salary(self) -> Decimal:
        """Calcula o salário diário (salário / 30)."""
        if self.is_employee and self.salary:
            return self.salary / Decimal("30")
        return self.daily_rate

    def validate(self) -> list:
        """Retorna lista de erros de validação do domínio."""
        errors = []
        if not self.name or len(self.name.strip()) < 3:
            errors.append("Nome deve ter ao menos 3 caracteres.")
        if self.is_employee and self.salary <= 0:
            errors.append("Funcionários CLT devem ter salário definido.")
        if self.is_daily_worker and self.daily_rate <= 0:
            errors.append("Diaristas devem ter valor de diária definido.")
        return errors