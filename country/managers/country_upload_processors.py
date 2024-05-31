import pandas as pd
import json
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)
from mt_economic_common.country.repositories.country_repository import CountryRepository
from mt_economic_common.country.repositories.country_oecd_repository import (
    CountryOecdFxAnnualRepository,
    CountryOecdInflationRepository,
    CountryOecdRepository,
)
from mt_economic_common.oecd_api.utils.sdmx_json_reader import SdmxJsonReader


class RestCountriesUploadProcessor:
    def __init__(self, api_upload_registry, session_data: dict):
        self.api_upload_registry = api_upload_registry
        self.session_data = session_data
        self.message = None

    def pre_check(self, json_response: dict | list) -> bool:
        return True

    def post_check(self, json_response: dict | list) -> bool:
        return True

    def process(self, json_response: dict | list) -> bool:
        countries_df = pd.read_json(json.dumps(json_response))
        countries_df["link_country_currency"] = self._create_currencies(
            countries_df["currencies"]
        )
        countries_df["country_name"] = countries_df["name"].apply(lambda x: x["common"])
        countries_df["country_official_name"] = countries_df["name"].apply(
            lambda x: x["official"]
        )
        countries_df["comment"] = f"Uploaded via REST Api"
        countries_df["country_lat"] = countries_df["latlng"].apply(
            lambda x: x[0] if x else None
        )
        countries_df["country_long"] = countries_df["latlng"].apply(
            lambda x: x[1] if x else None
        )
        countries_df["country_continent"] = countries_df["continents"].apply(
            lambda x: ", ".join(x) if x else None
        )
        countries_df["capital"] = countries_df["capital"].fillna("None")
        countries_df["country_capital"] = countries_df["capital"].apply(
            lambda x: ", ".join(x)
        )
        countries_df["country_postal_code_format"] = countries_df["postalCode"].apply(
            lambda x: self._get_json_field(x, "format")
        )
        countries_df["country_postal_code_regex"] = countries_df["postalCode"].apply(
            lambda x: self._get_json_field(x, "regex")
        )
        countries_df["country_google_maps_url"] = countries_df["maps"].apply(
            lambda x: x["googleMaps"] if x else None
        )
        countries_df["country_open_street_map_url"] = countries_df["maps"].apply(
            lambda x: x["openStreetMaps"] if x else None
        )
        countries_df["country_flag"] = countries_df["flags"].apply(
            lambda x: x["png"] if x else None
        )
        rename_columns = {
            "cca3": "country_code",
            "cca2": "country_code_2",
            "capital": "country_capital",
            "unMember": "country_un_member",
            "region": "country_region",
            "subregion": "country_subregion",
            "area": "country_area",
            "population": "country_population",
        }
        countries_df = countries_df.rename(columns=rename_columns)
        countries_df = countries_df.loc[
            :,
            [
                "country_name",
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
                "link_country_currency",
            ]
            + list(rename_columns.values()),
        ]
        try:
            CountryRepository(
                session_data=self.session_data
            ).create_objects_from_data_frame(countries_df)
            self.message = f"Successfully uploaded {len(countries_df)} countries"
        except Exception as e:
            self.message = (
                f"Error raised during object creation: {e.__class__.__name__}: {e}"
            )
            return False
        return True

    def _get_json_field(self, json_obj: dict | None, field_name: str):
        if pd.isnull(json_obj):
            return None
        return json_obj.get(field_name, None)

    def _create_currencies(self, currencies_series: pd.Series) -> pd.Series:
        def extract_currencies(data: list):
            return [
                {
                    "ccy_code": currency,
                    "ccy_name": details.get("name"),
                    "ccy_symbol": details.get("symbol"),
                }
                for currency, details in data.items()
            ]

        currencies_series = currencies_series.dropna()

        currency_list = [
            item
            for sublist in currencies_series.apply(extract_currencies)
            for item in sublist
        ]
        currency_df = pd.DataFrame(currency_list).drop_duplicates()
        currency_repository = CurrencyRepository(session_data=self.session_data)
        currency_repository.create_objects_from_data_frame(currency_df)
        currency_hubs = currency_repository.std_queryset().all()
        currency_hub_map = {c.ccy_code: c for c in currency_hubs}
        return pd.Series(
            currencies_series.apply(lambda x: [currency_hub_map[c] for c in x])
        )


class OecdCountriesUploadProcessor:
    repository_class = None
    value_field = ""

    def __init__(self, api_upload_registry, session_data: dict):
        self.api_upload_registry = api_upload_registry
        self.session_data = session_data
        self.repository = self.repository_class(session_data=session_data)
        self.message = None

    def pre_check(self, json_response: dict | list) -> bool:
        return True

    def post_check(self, json_response: dict | list) -> bool:
        return True

    def process(self, json_response: dict | list) -> bool:
        reader = SdmxJsonReader(json_data=json_response, dimension_out="id")
        data_df = reader.to_data_frame()
        data_df = self.convert_data_df(data_df)
        try:
            self.repository.create_objects_from_data_frame(data_df)
            self.message = f"Successfully uploaded {len(data_df)} data points"
        except Exception as e:
            self.message = (
                f"Error raised during object creation: {e.__class__.__name__}: {e}"
            )
            return False
        return True

    def convert_data_df(self, data_df: pd.DataFrame) -> pd.DataFrame:
        data_df = self._map_country_hub(data_df)
        data_df = self._prepare_df(data_df)
        return data_df

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
                "VALUE": self.value_field,
            }
        )
        df["value_date"] = pd.to_datetime(df["year"], format="%Y")
        return df.loc[
            ~pd.isnull(df["hub_entity_id"]),
            ["hub_entity_id", "year", self.value_field, "value_date"],
        ]


class OecdAnnualFxUploadProcessor(OecdCountriesUploadProcessor):
    value_field = "annual_fx_average"
    repository_class = CountryOecdFxAnnualRepository


class OecdInflationUploadProcessor(OecdCountriesUploadProcessor):
    value_field = "inflation"
    repository_class = CountryOecdInflationRepository
