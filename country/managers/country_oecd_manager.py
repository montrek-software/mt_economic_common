import pandas as pd
from baseclasses.managers.montrek_manager import MontrekManager
from reporting.managers.montrek_table_manager import MontrekTableManager
from mt_economic_common.country.repositories.country_oecd_repository import (
    CountryOecdRepository,
    CountryOecdTableRepository,
)
from mt_economic_common.oecd_api.managers.oecd_request_manager import OecdRequestManager
from reporting.dataclasses import table_elements as te


class CountryOecdManager(MontrekManager):
    repository_class = CountryOecdRepository

    def write_oecd_annual_fx_average_to_db(self):
        annual_fx_df = OecdRequestManager().get_average_annual_fx_rates()
        annual_fx_df = self._map_country_hub(annual_fx_df)
        annual_fx_df = self._prepare_df(annual_fx_df)
        self.repository.create_objects_from_data_frame(annual_fx_df)

    def _map_country_hub(self, df: pd.DataFrame) -> pd.DataFrame:
        unique_country_codes = df["REF_AREA"].unique()
        cnt_code_hub_map = {
            c.country_code: c.id
            for c in self.repository.std_queryset().filter(
                country_code__in=unique_country_codes
            )
        }
        df["REF_AREA"] = df["REF_AREA"].map(cnt_code_hub_map)
        return df

    def _prepare_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(
            columns={
                "REF_AREA": "hub_entity_id",
                "TIME_PERIOD": "year",
                "VALUE": "annual_fx_average",
            }
        )
        df["value_date"] = pd.to_datetime(df["year"], format="%Y")
        return df.loc[
            ~pd.isnull(df["hub_entity_id"]),
            ["hub_entity_id", "year", "annual_fx_average", "value_date"],
        ]


class YearTableElement(te.IntTableElement):
    def _format_value(self, value: int) -> str:
        return str(value)


class CountryOecdTableManager(MontrekTableManager):
    repository_class = CountryOecdTableRepository

    @property
    def table_elements(self) -> list:
        return [
            YearTableElement(name="Year", attr="year"),
            te.FloatTableElement(name="Annual FX Average", attr="annual_fx_average"),
        ]
