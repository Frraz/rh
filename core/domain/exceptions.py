"""
Exceções do domínio.
Todas as exceções de regras de negócio herdam daqui.
"""


class DomainException(Exception):
    """Exceção base para erros de domínio."""
    default_message = "Erro de domínio."

    def __init__(self, message: str = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class EntityNotFoundException(DomainException):
    """Lançada quando uma entidade não é encontrada."""
    default_message = "Entidade não encontrada."


class BusinessRuleViolationException(DomainException):
    """Lançada quando uma regra de negócio é violada."""
    default_message = "Regra de negócio violada."


class InvalidValueException(DomainException):
    """Lançada quando um valor fornecido é inválido."""
    default_message = "Valor inválido."


class PermissionDeniedException(DomainException):
    """Lançada quando o usuário não tem permissão para a operação."""
    default_message = "Permissão negada."


class DuplicateEntityException(DomainException):
    """Lançada quando se tenta criar uma entidade duplicada."""
    default_message = "Registro já existe."