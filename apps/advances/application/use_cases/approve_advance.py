"""Caso de uso: Aprovar adiantamento."""
import logging
from django.utils import timezone
from core.application.use_cases.base import UseCase
from core.domain.exceptions import BusinessRuleViolationException
from ...infrastructure.models import Advance
from apps.attendance.infrastructure.models import Adjustment

logger = logging.getLogger(__name__)


class ApproveAdvanceUseCase(UseCase):
    """
    Aprova um adiantamento e gera automaticamente
    o ajuste de desconto no mês de referência.
    """

    def execute(self, advance_id: int, approved_value, discount_year: int,
                discount_month: int, reviewed_by) -> Advance:

        try:
            advance = Advance.objects.select_related("person").get(pk=advance_id)
        except Advance.DoesNotExist:
            raise BusinessRuleViolationException("Adiantamento não encontrado.")

        if advance.status != Advance.Status.PENDING:
            raise BusinessRuleViolationException(
                "Apenas adiantamentos pendentes podem ser aprovados."
            )

        if approved_value <= 0:
            raise BusinessRuleViolationException("Valor aprovado deve ser positivo.")

        # Gera o ajuste de desconto
        adjustment = Adjustment.objects.create(
            person=advance.person,
            adjustment_type=Adjustment.AdjustmentType.ADVANCE,
            reference_year=discount_year,
            reference_month=discount_month,
            event_date=advance.request_date,
            value=-abs(approved_value),  # Negativo = desconto
            origin=Adjustment.Origin.ADVANCE_MODULE,
            description=f"Desconto de adiantamento aprovado em {timezone.now().strftime('%d/%m/%Y')}",
            created_by=reviewed_by,
        )

        advance.approved_value = approved_value
        advance.discount_reference_year = discount_year
        advance.discount_reference_month = discount_month
        advance.status = Advance.Status.APPROVED
        advance.reviewed_by = reviewed_by
        advance.reviewed_at = timezone.now()
        advance.generated_adjustment = adjustment
        advance.save()

        logger.info(
            "Adiantamento aprovado: id=%s colaborador=%s valor=%.2f",
            advance.pk, advance.person.name, approved_value,
        )
        return advance