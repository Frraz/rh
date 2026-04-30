"""Entidades de domínio do módulo de contas."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    ADMIN = "admin"
    HR = "hr"
    MANAGER = "manager"
    EMPLOYEE = "employee"

    @property
    def display(self) -> str:
        labels = {
            "admin": "Administrador",
            "hr": "RH",
            "manager": "Gestor",
            "employee": "Colaborador",
        }
        return labels[self.value]


@dataclass
class UserEntity:
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    entity_id: Optional[int] = None

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    @property
    def is_hr(self) -> bool:
        return self.role in (UserRole.ADMIN, UserRole.HR)

    @property
    def is_manager(self) -> bool:
        return self.role in (UserRole.ADMIN, UserRole.HR, UserRole.MANAGER)