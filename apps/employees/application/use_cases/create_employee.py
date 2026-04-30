"""Caso de uso: Criar colaborador."""
import logging
from core.application.use_cases.base import UseCase
from core.shared.utils.cpf_utils import validate_cpf, clean_cpf
from ..dtos import CreatePersonDTO
from ...infrastructure.models import Person
from ...domain.exceptions import DuplicateCPFException, InvalidPersonDataException

logger = logging.getLogger(__name__)


class CreatePersonUseCase(UseCase):
    """
    Cria um novo colaborador (funcionário ou diarista).
    Responsável por validações de domínio antes da persistência.
    """

    def execute(self, dto: CreatePersonDTO) -> Person:
        # 1. Validar CPF
        clean = clean_cpf(dto.cpf)
        if not validate_cpf(clean):
            raise InvalidPersonDataException("CPF inválido.")

        # 2. Verificar duplicidade de CPF na entidade
        if Person.all_objects.filter(cpf=clean, entity_id=dto.entity_id).exists():
            raise DuplicateCPFException(
                f"Já existe um colaborador com CPF {dto.cpf} nesta entidade."
            )

        # 3. Validar remuneração
        if dto.person_type == "employee" and dto.salary <= 0:
            raise InvalidPersonDataException(
                "Funcionários CLT devem ter salário definido."
            )
        if dto.person_type == "daily" and dto.daily_rate <= 0:
            raise InvalidPersonDataException(
                "Diaristas devem ter valor de diária definido."
            )

        # 4. Persistir
        person = Person.objects.create(
            name=dto.name.strip(),
            cpf=clean,
            person_type=dto.person_type,
            entity_id=dto.entity_id,
            farm_id=dto.farm_id,
            job_role_id=dto.job_role_id,
            admission_date=dto.admission_date,
            salary=dto.salary,
            daily_rate=dto.daily_rate,
            phone=dto.phone,
            birth_date=dto.birth_date,
            rg=dto.rg,
            pis=dto.pis,
            ctps=dto.ctps,
            marital_status=dto.marital_status,
            address=dto.address,
            bank=dto.bank,
            bank_agency=dto.bank_agency,
            bank_account=dto.bank_account,
            notes=dto.notes,
        )

        logger.info("Colaborador criado: id=%s nome=%s", person.id, person.name)
        return person