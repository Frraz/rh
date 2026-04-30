"""Data Transfer Objects para o módulo de funcionários."""
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class CreatePersonDTO:
    name: str
    cpf: str
    person_type: str
    entity_id: int
    farm_id: int
    job_role_id: int
    admission_date: date
    salary: Decimal = Decimal("0.00")
    daily_rate: Decimal = Decimal("0.00")
    phone: str = ""
    birth_date: Optional[date] = None
    rg: str = ""
    pis: str = ""
    ctps: str = ""
    marital_status: str = ""
    address: str = ""
    bank: str = ""
    bank_agency: str = ""
    bank_account: str = ""
    notes: str = ""


@dataclass
class UpdatePersonDTO:
    person_id: int
    name: str
    farm_id: int
    job_role_id: int
    phone: str = ""
    birth_date: Optional[date] = None
    salary: Decimal = Decimal("0.00")
    daily_rate: Decimal = Decimal("0.00")
    rg: str = ""
    marital_status: str = ""
    address: str = ""
    bank: str = ""
    bank_agency: str = ""
    bank_account: str = ""
    notes: str = ""


@dataclass
class PersonOutputDTO:
    id: int
    name: str
    cpf: str
    person_type: str
    person_type_display: str
    status: str
    status_display: str
    entity_name: str
    farm_name: str
    job_role_name: str
    admission_date: date
    salary: Decimal
    daily_rate: Decimal
    phone: str
    is_employee: bool
    is_daily_worker: bool