"""Utilitários de moeda e valores monetários (Real Brasileiro)."""
from decimal import Decimal, ROUND_HALF_UP


def to_decimal(value) -> Decimal:
    """Converte valor para Decimal com precisão adequada."""
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def round_currency(value: Decimal) -> Decimal:
    """Arredonda para 2 casas decimais no padrão monetário brasileiro."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def format_brl(value: Decimal) -> str:
    """Formata Decimal como moeda BRL: R$ 1.234,56"""
    value = round_currency(value)
    formatted = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatted}"


def percentage_of(value: Decimal, percentage: Decimal) -> Decimal:
    """Calcula percentual de um valor e arredonda."""
    return round_currency(value * percentage / Decimal("100"))