import logging
from dataclasses import dataclass
from decimal import Decimal
from django.utils import timezone
from core.application.use_cases.base import UseCase
from core.domain.exceptions import BusinessRuleViolationException

logger = logging.getLogger(__name__)


@dataclass
class CreateInstallmentDTO:
    person_id: int
    installment_type: str
    description: str
    total_value: Decimal
    num_installments: int
    first_reference_year: int
    first_reference_month: int
    created_by_id: int = None


def next_month(year: int, month: int):
    if month == 12:
        return year + 1, 1
    return year, month + 1


class CreateInstallmentUseCase(UseCase):

    def execute(self, dto: CreateInstallmentDTO):
        from apps.attendance.infrastructure.models import Adjustment, DiscountInstallment
        from apps.employees.infrastructure.models import Person

        if dto.num_installments < 1 or dto.num_installments > 60:
            raise BusinessRuleViolationException("Número de parcelas deve ser entre 1 e 60.")
        if dto.total_value <= 0:
            raise BusinessRuleViolationException("Valor total deve ser positivo.")
        if dto.first_reference_month < 1 or dto.first_reference_month > 12:
            raise BusinessRuleViolationException("Mês de referência inválido.")

        try:
            person = Person.objects.get(pk=dto.person_id)
        except Person.DoesNotExist:
            raise BusinessRuleViolationException("Colaborador não encontrado.")

        installment_value = round(dto.total_value / dto.num_installments, 2)

        installment = DiscountInstallment.objects.create(
            person=person,
            installment_type=dto.installment_type,
            description=dto.description,
            total_value=dto.total_value,
            num_installments=dto.num_installments,
            installment_value=installment_value,
            first_reference_year=dto.first_reference_year,
            first_reference_month=dto.first_reference_month,
            created_by_id=dto.created_by_id,
        )

        year = dto.first_reference_year
        month = dto.first_reference_month
        today = timezone.localdate()

        for i in range(1, dto.num_installments + 1):
            if i == dto.num_installments:
                valor = dto.total_value - (installment_value * (dto.num_installments - 1))
            else:
                valor = installment_value

            Adjustment.objects.create(
                person=person,
                adjustment_type=Adjustment.AdjustmentType.INSTALLMENT,
                reference_year=year,
                reference_month=month,
                event_date=today,
                value=-abs(valor),
                origin=Adjustment.Origin.INSTALLMENT_MODULE,
                description=f"{dto.description} — parcela {i}/{dto.num_installments}",
                installment=installment,
                installment_number=i,
                created_by_id=dto.created_by_id,
            )
            year, month = next_month(year, month)

        logger.info("Parcelamento criado: pessoa=%s parcelas=%d valor=%.2f",
                    person.name, dto.num_installments, float(dto.total_value))
        return installment
