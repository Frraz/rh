"""Validação e formatação de CPF."""
import re


def format_cpf(cpf: str) -> str:
    """Formata CPF para 000.000.000-00."""
    digits = re.sub(r"\D", "", cpf)
    if len(digits) != 11:
        return cpf
    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"


def clean_cpf(cpf: str) -> str:
    """Remove formatação do CPF."""
    return re.sub(r"\D", "", cpf)


def validate_cpf(cpf: str) -> bool:
    """Valida CPF com algoritmo oficial."""
    digits = clean_cpf(cpf)
    if len(digits) != 11 or len(set(digits)) == 1:
        return False

    def calc_digit(digits, length):
        total = sum(int(d) * w for d, w in zip(digits, range(length + 1, 1, -1)))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    if int(digits[9]) != calc_digit(digits, 9):
        return False
    if int(digits[10]) != calc_digit(digits, 10):
        return False
    return True