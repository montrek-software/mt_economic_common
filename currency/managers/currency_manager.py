from baseclasses.managers.montrek_manager import MontrekManager
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)


class CurrencyManager(MontrekManager):
    repository_class = CurrencyRepository
