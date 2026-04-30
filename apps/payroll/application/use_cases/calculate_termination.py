"""
Caso de uso: Calcular rescisão contratual.
Implementa as regras da CLT para cálculo de verbas rescisórias.
"""
import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from core.application.use_cases.base import UseCase
from core.shared.utils.date_utils import (
    calculate_months_between, days_in_month, get_reference_month_display
)
from core.shared.utils.currency_utils import round_currency, percentage_of

logger = logging.getLogger(__name__)


@dataclass
class TerminationInputDTO:
    person_id: int
    termination_type: str
    termination_date: date
    notice_type: str  # "worked" | "waived" | "none"
    vacation_days_due: int      # Dias de férias vencidas
    vacation_months_prop: int   # Meses trabalhados no período aquisitivo atual
    fgts_balance: Decimal       # Saldo FGTS depositado (informado pelo usuário)


@dataclass
class TerminationOutputDTO:
    person_name: str
    termination_type_display: str
    termination_date: date
    admission_date: date
    salary: Decimal

    # Itens calculados
    balance_days: int
    balance_value: Decimal
    vacation_due_value: Decimal
    vacation_prop_value: Decimal
    vacation_bonus: Decimal
    thirteenth_value: Decimal
    fgts_balance: Decimal
    fgts_fine: Decimal
    gross_total: Decimal
    inss_value: Decimal
    net_total: Decimal

    # Memória de cálculo (para auditoria e PDF)
    memory: dict


# Tabela INSS 2024
INSS_TABLE = [
    (Decimal("1412.00"), Decimal("7.5")),
    (Decimal("2666.68"), Decimal("9.0")),
    (Decimal("4000.03"), Decimal("12.0")),
    (Decimal("7786.02"), Decimal("14.0")),
]


def calculate_inss(salary: Decimal) -> Decimal:
    """Calcula INSS progressivo conforme tabela vigente."""
    inss = Decimal("0")
    prev_limit = Decimal("0")
    for limit, rate in INSS_TABLE:
        if salary <= prev_limit:
            break
        taxable = min(salary, limit) - prev_limit
        inss += percentage_of(taxable, rate)
        prev_limit = limit
    return round_currency(inss)


class CalculateTerminationUseCase(UseCase):

    def execute(self, dto: TerminationInputDTO) -> TerminationOutputDTO:
        from apps.employees.infrastructure.models import Person

        try:
            person = Person.objects.get(pk=dto.person_id)
        except Person.DoesNotExist:
            raise ValueError("Colaborador não encontrado.")

        salary = person.salary
        admission = person.admission_date
        termination = dto.termination_date

        # 1. Saldo de salário (dias trabalhados no mês da demissão)
        balance_days = termination.day
        daily_salary = round_currency(salary / Decimal("30"))
        balance_value = round_currency(daily_salary * balance_days)

        # 2. Férias vencidas (se houver)
        vacation_due_value = Decimal("0")
        if dto.vacation_days_due > 0:
            vacation_due_value = round_currency(salary * dto.vacation_days_due / Decimal("30"))

        # 3. Férias proporcionais
        vacation_prop_months = dto.vacation_months_prop
        vacation_prop_value = round_currency(salary * vacation_prop_months / Decimal("12"))

        # 4. 1/3 sobre férias (vencidas + proporcionais)
        total_vacation = vacation_due_value + vacation_prop_value
        vacation_bonus = round_currency(total_vacation / Decimal("3"))

        # 5. 13º proporcional
        months_in_year = calculate_months_between(
            date(termination.year, 1, 1), termination
        ) + 1  # mês atual conta
        thirteenth_value = round_currency(salary * min(months_in_year, 12) / Decimal("12"))

        # 6. FGTS (multa 40% para demissão sem justa causa)
        fgts_fine = Decimal("0")
        if dto.termination_type == "without_cause":
            fgts_fine = round_currency(dto.fgts_balance * Decimal("0.40"))

        # 7. Total bruto e INSS
        gross_total = (
            balance_value + vacation_due_value + vacation_prop_value
            + vacation_bonus + thirteenth_value + fgts_fine
        )
        # INSS incide sobre saldo + férias + 13º (não sobre multa FGTS)
        inss_base = balance_value + vacation_due_value + vacation_prop_value + thirteenth_value
        inss_value = calculate_inss(inss_base)
        net_total = round_currency(gross_total - inss_value)

        memory = {
            "salary": str(salary),
            "admission_date": str(admission),
            "termination_date": str(termination),
            "daily_salary": str(daily_salary),
            "balance_days": balance_days,
            "balance_value": str(balance_value),
            "vacation_days_due": dto.vacation_days_due,
            "vacation_due_value": str(vacation_due_value),
            "vacation_prop_months": vacation_prop_months,
            "vacation_prop_value": str(vacation_prop_value),
            "vacation_bonus": str(vacation_bonus),
            "thirteenth_months": months_in_year,
            "thirteenth_value": str(thirteenth_value),
            "fgts_balance": str(dto.fgts_balance),
            "fgts_fine": str(fgts_fine),
            "gross_total": str(gross_total),
            "inss_base": str(inss_base),
            "inss_value": str(inss_value),
            "net_total": str(net_total),
        }

        return TerminationOutputDTO(
            person_name=person.name,
            termination_type_display=dto.termination_type,
            termination_date=termination,
            admission_date=admission,
            salary=salary,
            balance_days=balance_days,
            balance_value=balance_value,
            vacation_due_value=vacation_due_value,
            vacation_prop_value=vacation_prop_value,
            vacation_bonus=vacation_bonus,
            thirteenth_value=thirteenth_value,
            fgts_balance=dto.fgts_balance,
            fgts_fine=fgts_fine,
            gross_total=gross_total,
            inss_value=inss_value,
            net_total=net_total,
            memory=memory,
        )