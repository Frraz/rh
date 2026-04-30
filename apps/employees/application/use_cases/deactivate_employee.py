"""Caso de uso: Desativar colaborador."""
import logging
from core.application.use_cases.base import UseCase
from ...infrastructure.models import Person
from ...domain.exceptions import PersonNotFoundException

logger = logging.getLogger(__name__)


class DeactivatePersonUseCase(UseCase):

    def execute(self, person_id: int) -> Person:
        try:
            person = Person.objects.get(pk=person_id)
        except Person.DoesNotExist:
            raise PersonNotFoundException()

        person.status = Person.Status.INACTIVE
        person.save(update_fields=["status", "updated_at"])

        logger.info("Colaborador desativado: id=%s nome=%s", person.id, person.name)
        return person