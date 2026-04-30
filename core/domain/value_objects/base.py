"""
Value Object base do domínio.
Value Objects são imutáveis e identificados por seus atributos.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    """
    Classe base para Value Objects.
    São imutáveis (frozen=True) e comparados por valor.
    """
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"