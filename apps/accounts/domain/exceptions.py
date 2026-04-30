from core.domain.exceptions import DomainException


class InvalidCredentialsException(DomainException):
    default_message = "Credenciais inválidas."


class UserAlreadyExistsException(DomainException):
    default_message = "Usuário já existe com este e-mail ou nome de usuário."


class UserNotFoundException(DomainException):
    default_message = "Usuário não encontrado."


class InactiveUserException(DomainException):
    default_message = "Conta de usuário inativa."