"""
Caso de uso base da camada de aplicação.
Define o contrato padrão para todos os casos de uso do sistema.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
import logging

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")

logger = logging.getLogger(__name__)


class BaseUseCase(ABC, Generic[InputDTO, OutputDTO]):
    """
    Classe base para casos de uso.
    Cada caso de uso representa uma única ação de negócio.
    """

    @abstractmethod
    def execute(self, input_dto: InputDTO) -> OutputDTO:
        """
        Executa o caso de uso.
        Deve conter a lógica de orquestração sem acoplamento à infraestrutura.
        """
        raise NotImplementedError


class UseCase(ABC):
    """
    Variante de caso de uso sem tipagem genérica.
    Útil para casos de uso com assinaturas mais variadas.
    """

    def __call__(self, *args, **kwargs):
        return self.execute(*args, **kwargs)

    @abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError