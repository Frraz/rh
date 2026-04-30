from core.domain.exceptions import DomainException


class PersonNotFoundException(DomainException):
    default_message = "Colaborador não encontrado."


class DuplicateCPFException(DomainException):
    default_message = "Já existe um colaborador com este CPF."


class InvalidPersonDataException(DomainException):
    default_message = "Dados do colaborador inválidos."


class EntityNotFoundException(DomainException):
    default_message = "Entidade não encontrada."


class CannotDeactivatePersonException(DomainException):
    default_message = "Não é possível desativar este colaborador."