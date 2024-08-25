from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_economic_common.country.models import CountryHub


class CountryReportRepository(MontrekRepository):
    hub_class = CountryHub

    def std_queryset(self):
        return self.build_queryset()
