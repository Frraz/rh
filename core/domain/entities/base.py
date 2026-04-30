"""
Entidade base do domínio.
Define a estrutura fundamental de identidade de uma entidade de domínio.
Entidades são identificadas por seu ID, não por seus atributos.
"""
from dataclasses import dataclass, field
from typing import Any
import uuid


@dataclass
class Entity:
    """
    Classe base para entidades de domínio.
    Toda entidade possui identidade única e imutável.
    """
    id: Any = field(default_factory=uuid.uuid4)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"