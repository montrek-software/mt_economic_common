from typing import Any

import pandas as pd
from data_import.api_import.managers.api_data_import_processor import (
    ApiDataImportProcessorBase,
)
from data_import.types import ImportDataType
from django.conf import settings
from mt_economic_common.country.managers.country_request_manager import (
    RestCountriesRequestManager,
)
from mt_economic_common.country.repositories.country_oecd_repository import (
    CountryOecdFxAnnualRepository,
    CountryOecdInflationRepository,
)
from mt_economic_common.country.repositories.country_repository import CountryRepository
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)
from mt_economic_common.sdmx_api.managers.sdmx_request_manager import (
    OecdSdmxRequestManager,
)


class RestCountriesUploadProcessor(ApiDataImportProcessorBase):
    request_manager_class = RestCountriesRequestManager
    endpoint = ""

    def post_check(self) -> bool:
        return True

    def apply_import_data(self) -> bool:
        try:
            countries_df = pd.DataFrame(self.import_data)
            countries_df["country_code"] = countries_df["codes"].apply(
                lambda x: self._get_json_field(x, "alpha_3")
            )
            countries_df["country_code_2"] = countries_df["codes"].apply(
                lambda x: self._get_json_field(x, "alpha_2")
            )
            # Entities without ISO codes (e.g. Abkhazia) were not part of the
            # legacy API and cannot be identified by country_code
            countries_df = countries_df.loc[
                countries_df["country_code"].notna()
            ].reset_index(drop=True)
            countries_df["link_country_currency"] = self.create_currencies(
                countries_df["currencies"]
            )
            countries_df["country_name"] = countries_df["names"].apply(
                lambda x: self._get_json_field(x, "common")
            )
            countries_df["country_official_name"] = countries_df["names"].apply(
                lambda x: self._get_json_field(x, "official")
            )
            countries_df["comment"] = "Uploaded via REST Api"
            countries_df["country_lat"] = countries_df["coordinates"].apply(
                lambda x: self._get_json_field(x, "lat")
            )
            countries_df["country_long"] = countries_df["coordinates"].apply(
                lambda x: self._get_json_field(x, "lng")
            )
            countries_df["country_continent"] = countries_df["continents"].apply(
                self._join_list
            )
            countries_df["country_capital"] = countries_df["capitals"].apply(
                lambda x: self._join_list(
                    [capital["name"] for capital in x] if isinstance(x, list) else x
                )
            )
            countries_df["country_postal_code_format"] = countries_df[
                "postal_code"
            ].apply(lambda x: self._get_json_field(x, "format"))
            countries_df["country_postal_code_regex"] = countries_df[
                "postal_code"
            ].apply(lambda x: self._get_json_field(x, "regex"))
            countries_df["country_google_maps_url"] = countries_df["links"].apply(
                lambda x: self._get_json_field(x, "google_maps")
            )
            countries_df["country_open_street_map_url"] = countries_df["links"].apply(
                lambda x: self._get_json_field(x, "open_street_maps")
            )
            countries_df["country_flag"] = countries_df["flag"].apply(
                lambda x: self._get_json_field(x, "url_png")
            )
            countries_df["country_un_member"] = countries_df["classification"].apply(
                lambda x: self._get_json_field(x, "un_member")
            )
            countries_df["country_area"] = countries_df["area"].apply(
                lambda x: self._get_json_field(x, "kilometers")
            )
            rename_columns = {
                "region": "country_region",
                "subregion": "country_subregion",
                "population": "country_population",
            }
            countries_df = countries_df.rename(columns=rename_columns)
            for column in ("country_region", "country_subregion"):
                countries_df[column] = countries_df[column].apply(lambda x: x or None)
            countries_df = countries_df.loc[
                :,
                [
                    "country_code",
                    "country_code_2",
                    "country_name",
                    "country_capital",
                    "country_official_name",
                    "comment",
                    "country_lat",
                    "country_long",
                    "country_continent",
                    "country_postal_code_format",
                    "country_postal_code_regex",
                    "country_google_maps_url",
                    "country_open_street_map_url",
                    "country_flag",
                    "country_un_member",
                    "country_area",
                    "link_country_currency",
                ]
                + list(rename_columns.values()),
            ]
        except (KeyError, ValueError, TypeError) as e:
            if settings.IS_TEST_RUN:
                raise e
            self.set_message(
                f"Error raised during DataFrame transformation: {e.__class__.__name__}: {e}"
            )
            return False
        try:
            CountryRepository(
                session_data=self.session_data
            ).create_objects_from_data_frame(countries_df)
            self.set_message(f"Successfully uploaded {len(countries_df)} countries")
        except Exception as e:
            if settings.IS_TEST_RUN:
                raise e
            self.set_message(
                f"Error raised during object creation: {e.__class__.__name__}: {e}"
            )
            return False
        return True

    @staticmethod
    def _get_json_field(json_obj: dict | None, field_name: str):
        if not isinstance(json_obj, dict):
            return None
        value = json_obj.get(field_name)
        # The API returns empty strings for missing values
        if value == "":
            return None
        return value

    @staticmethod
    def _join_list(values: list | None) -> str | None:
        if not isinstance(values, list) or not values:
            return None
        return ", ".join(values)

    def create_currencies(self, currencies_series: pd.Series) -> pd.Series:
        currencies_series = currencies_series.apply(
            lambda x: x if isinstance(x, list) else []
        )
        currency_list = [
            {
                "ccy_code": currency["code"],
                "ccy_name": currency.get("name"),
                "ccy_symbol": currency.get("symbol"),
            }
            for currencies in currencies_series
            for currency in currencies
        ]
        if currency_list:
            currency_df = pd.DataFrame(currency_list).drop_duplicates(
                subset=["ccy_code"]
            )
            currency_repository = CurrencyRepository(session_data=self.session_data)
            currency_repository.create_objects_from_data_frame(currency_df)
        currency_hub_map = {
            c.ccy_code: c
            for c in CurrencyRepository(session_data=self.session_data).receive().all()
        }
        return currencies_series.apply(
            lambda x: [currency_hub_map[currency["code"]] for currency in x]
        )


class OecdCountriesUploadProcessor(ApiDataImportProcessorBase):
    repository_class = None
    request_manager_class = OecdSdmxRequestManager
    value_field = ""

    def __init__(self, session_data: dict[str, Any], import_data: ImportDataType):
        super().__init__(session_data, import_data)
        self.repository = self.repository_class(self.session_data)

    def post_check(self) -> bool:
        return True

    def process(self) -> bool:
        response_df = self.import_data
        data_df = self.convert_data_df(response_df)
        try:
            self.repository.create_objects_from_data_frame(data_df)
            self.set_message(f"Successfully uploaded {len(data_df)} data points")
        except Exception as e:
            if settings.IS_TEST_RUN:
                raise e
            self.set_message(
                f"Error raised during object creation: {e.__class__.__name__}: {e}"
            )
            return False
        return True

    def convert_data_df(self, data_df: pd.DataFrame) -> pd.DataFrame:
        data_df = data_df.reset_index()
        data_df = self._map_country_hub(data_df)
        data_df = self._prepare_df(data_df)
        return data_df

    def _map_country_hub(self, df: pd.DataFrame) -> pd.DataFrame:
        unique_country_codes = df["REF_AREA"].unique()
        cnt_code_hub_map = {
            c.country_code: c.hub.id
            for c in self.repository.receive().filter(
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
                "value": self.value_field,
            }
        )
        df["value_date"] = df["year"].apply(lambda x: f"{x}-12-31")
        df["value_date"] = pd.to_datetime(df["value_date"])
        return df.loc[
            ~pd.isnull(df["hub_entity_id"]),
            ["hub_entity_id", "year", self.value_field, "value_date"],
        ]


class OecdAnnualFxUploadProcessor(OecdCountriesUploadProcessor):
    value_field = "annual_fx_average"
    repository_class = CountryOecdFxAnnualRepository
    endpoint = "OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE4,/A....EXC_A.......?startPeriod=2000&dimensionAtObservation=AllDimensions"


class OecdInflationUploadProcessor(OecdCountriesUploadProcessor):
    value_field = "inflation"
    repository_class = CountryOecdInflationRepository
    endpoint = (
        "OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL,1.0/.A.N.CPI.IX._T.N.?startPeriod=2000"
    )
