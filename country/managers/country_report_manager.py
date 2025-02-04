from requesting.managers.request_manager import RequestJsonManager
from django_pandas.io import read_frame
from mt_economic_common.country.managers.country_manager import (
    CountryDetailsManager,
)
from mt_economic_common.country.repositories.country_oecd_repository import (
    CountryOecdTableRepository,
)
from mt_economic_common.country.repositories.country_report_repository import (
    CountryReportRepository,
)
from reporting.core import reporting_text as rt
from reporting.core.reporting_data import ReportingData
from reporting.core.reporting_grid_layout import ReportGridLayout
from reporting.core.reporting_plots import ReportingPlot
from reporting.managers.montrek_report_manager import (
    MontrekReportManager,
)


class WikipediaRequestManager(RequestJsonManager):
    base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"


class CountryReportManager(MontrekReportManager):
    repository_class = CountryReportRepository

    def __init__(self, session_data):
        super().__init__(session_data)
        if "pk" in session_data:
            self.obj = self.repository.receive().get(pk=session_data["pk"])
        else:
            self.obj = None

    @property
    def document_title(self) -> str:
        return f"Country Report: {self.obj.country_name}"

    def collect_report_elements(self):
        self.append_report_element(rt.ReportingHeader1("Country Details"))
        self.append_report_element(CountryDetailsManager(self.session_data))
        self.append_report_element(rt.ReportingHeader1("Country Information"))
        self.append_report_element(rt.ReportingParagraph(self.get_wikipedia_section()))
        self.append_report_element(rt.ReportingHeader1("OECD Data"))
        self._plot_oecd_data()

    def get_wikipedia_section(self):
        country_summary = WikipediaRequestManager(self.session_data).get_response(
            self.obj.country_name
        )
        return country_summary.get("extract", "No summary found")

    def _plot_oecd_data(self):
        plot_grid = ReportGridLayout(1, 2)
        oecd_data = CountryOecdTableRepository(self.session_data).receive()
        oecd_df = read_frame(oecd_data)
        oecd_df = oecd_df.sort_values("value_date")
        oecd_reporting_data = ReportingData(
            oecd_df,
            "Annual FX Average",
            "year",
            y_axis_columns=["annual_fx_average"],
            plot_types=["line"],
        )
        plot = ReportingPlot(width=plot_grid.width)
        plot.generate(oecd_reporting_data)
        plot_grid.add_report_grid_element(plot, 0, 0)
        oecd_reporting_data = ReportingData(
            oecd_df,
            "Inflation",
            "year",
            y_axis_columns=["inflation"],
            plot_types=["line"],
        )
        plot = ReportingPlot(width=plot_grid.width)
        plot.generate(oecd_reporting_data)
        plot_grid.add_report_grid_element(plot, 0, 1)
        self.append_report_element(plot_grid)
