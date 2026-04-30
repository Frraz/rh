"""Utilitários de datas para o domínio brasileiro."""
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import calendar


def get_last_day_of_month(year: int, month: int) -> date:
    """Retorna o último dia do mês informado."""
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, last_day)


def get_reference_month_display(year: int, month: int) -> str:
    """Retorna string formatada: 'Janeiro/2024'"""
    month_names = [
        "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
    ]
    return f"{month_names[month]}/{year}"


def calculate_months_between(start: date, end: date) -> int:
    """Calcula quantidade de meses completos entre duas datas."""
    delta = relativedelta(end, start)
    return delta.years * 12 + delta.months


def calculate_years_of_service(admission_date: date, reference_date: date = None) -> float:
    """Calcula anos de serviço como float."""
    if reference_date is None:
        reference_date = date.today()
    delta = relativedelta(reference_date, admission_date)
    return delta.years + delta.months / 12


def days_in_month(year: int, month: int) -> int:
    """Retorna número de dias no mês."""
    return calendar.monthrange(year, month)[1]


def proportion_of_month(start: date, end: date) -> float:
    """
    Calcula proporção de um mês trabalhado.
    Usado para férias, 13º e saldo de salário proporcionais.
    """
    total_days = days_in_month(start.year, start.month)
    worked_days = (end - start).days + 1
    return min(worked_days / total_days, 1.0)