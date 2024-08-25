from mt_economic_common.country.managers.country_manager import (
    CountryDetailsManager,
)
from mt_economic_common.country.repositories.country_report_repository import (
    CountryReportRepository,
)
from reporting.core import reporting_text as rt
from reporting.managers.montrek_report_manager import (
    MontrekReportManager,
)


class CountryReportManager(MontrekReportManager):
    repository_class = CountryReportRepository

    def __init__(self, session_data):
        super().__init__(session_data)
        if "pk" in session_data:
            self.obj = self.repository.std_queryset().get(pk=session_data["pk"])
        else:
            self.obj = None

    @property
    def document_title(self) -> str:
        return f"Country Report: {self.obj.country_name}"

    def collect_report_elements(self):
        self.append_report_element(rt.ReportingHeader1("Country Details"))
        self.append_report_element(CountryDetailsManager(self.session_data))
        self.append_report_element(rt.ReportingHeader1("Country Informations"))

        self.append_report_element(rt.ReportingParagraph("Blummsi"))
