"""
Repositório base do domínio.
Define o contrato (interface) que toda implementação de repositório deve seguir.
A camada de domínio depende desta abstração, nunca da implementação concreta.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")
ID = TypeVar("ID")


class BaseRepository(ABC, Generic[T, ID]):
    """Interface base para repositórios de domínio."""

    @abstractmethod
    def get_by_id(self, entity_id: ID) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def save(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: ID) -> None:
        raise NotImplementedError