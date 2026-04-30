"""Caso de uso: Atualizar colaborador."""
import logging
from core.application.use_cases.base import UseCase
from ..dtos import UpdatePersonDTO
from ...infrastructure.models import Person
from ...domain.exceptions import PersonNotFoundException

logger = logging.getLogger(__name__)


class UpdatePersonUseCase(UseCase):

    def execute(self, dto: UpdatePersonDTO) -> Person:
        try:
            person = Person.objects.get(pk=dto.person_id)
        except Person.DoesNotExist:
            raise PersonNotFoundException(f"Colaborador id={dto.person_id} não encontrado.")

        person.name = dto.name.strip()
        person.farm_id = dto.farm_id
        person.job_role_id = dto.job_role_id
        person.phone = dto.phone
        person.birth_date = dto.birth_date
        person.salary = dto.salary
        person.daily_rate = dto.daily_rate
        person.rg = dto.rg
        person.marital_status = dto.marital_status
        person.address = dto.address
        person.bank = dto.bank
        person.bank_agency = dto.bank_agency
        person.bank_account = dto.bank_account
        person.notes = dto.notes
        person.save()

        logger.info("Colaborador atualizado: id=%s", person.id)
        return person