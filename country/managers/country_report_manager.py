from reporting.managers.montrek_report_manager import (
    MontrekReportManager,
)
from mt_economic_common.country.repositories.country_report_repository import (
    CountryReportRepository,
)


class CountryReportManager(MontrekReportManager):
    repository_class = CountryReportRepository
