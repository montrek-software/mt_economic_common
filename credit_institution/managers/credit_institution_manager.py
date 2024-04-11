from baseclasses.managers.montrek_manager import MontrekManager
from mt_economic_common.credit_institution.repositories.credit_institution_repository import (
    CreditInstitutionRepository,
)


class CreditInstitutionManager(MontrekManager):
    repository_class = CreditInstitutionRepository
