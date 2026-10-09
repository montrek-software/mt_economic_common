import pandas as pd
from reporting.core import reporting_text as rt
from reporting.core.reporting_data import ReportingData
from reporting.core.reporting_plots import ReportingPlot
from reporting.dataclasses.table_elements import DateTableElement
from reporting.managers.montrek_report_manager import MontrekReportManager
from reporting.managers.montrek_table_manager import MontrekTableManager

from mt_economic_common.currency.table_elements import FxRateTableElement
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyFxRateHistoryRepository,
    CurrencyRepository,
)


class CurrencyFxRateHistoryTableManager(MontrekTableManager):
    repository_class = CurrencyFxRateHistoryRepository

    @property
    def table_elements(self) -> tuple:
        return (
            DateTableElement(name="Value Date", attr="value_date"),
            FxRateTableElement(name="FX Rate", attr="fx_rate"),
        )


class CurrencyReportManager(MontrekReportManager):
    repository_class = CurrencyRepository

    def __init__(self, session_data: dict) -> None:
        super().__init__(session_data)
        self.obj = self.repository.receive().get(pk=session_data["pk"])
        self.history_manager = CurrencyFxRateHistoryTableManager(session_data)

    @property
    def document_title(self) -> str:
        return f"FX Rates: {self.obj.ccy_name} ({self.obj.ccy_code})"

    def collect_report_elements(self) -> None:
        self.append_report_element(rt.ReportingHeader1("FX Rate History"))
        self.append_report_element(
            rt.ReportingParagraph(f"Value of one {self.obj.ccy_code} in EUR.")
        )
        self.append_report_element(self._get_fx_rate_plot())
        self.append_report_element(self.history_manager)

    def _get_fx_rate_plot(self) -> ReportingPlot:
        fx_rates_df = pd.DataFrame(
            self.history_manager.repository.receive().values("value_date", "fx_rate"),
            columns=["value_date", "fx_rate"],
        )
        fx_rates_df = fx_rates_df.dropna(subset=["fx_rate"]).sort_values("value_date")
        fx_rates_df["fx_rate"] = fx_rates_df["fx_rate"].astype(float)
        plot = ReportingPlot()
        plot.generate(
            ReportingData(
                data_df=fx_rates_df,
                title=f"{self.obj.ccy_code} in EUR",
                x_axis_column="value_date",
                y_axis_columns=["fx_rate"],
                plot_types=["line"],
            )
        )
        return plot
