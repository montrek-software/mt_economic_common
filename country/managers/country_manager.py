import pandas as pd
import numpy as np
import json
from baseclasses.managers.montrek_manager import MontrekManager
from reporting.managers.montrek_table_manager import MontrekTableManager
from reporting.managers.montrek_details_manager import MontrekDetailsManager
from mt_economic_common.country.repositories.country_repository import CountryRepository
from mt_economic_common.country.managers.country_request_manager import (
    CountryRequestManager,
    RestCountriesRequestManager,
)
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)
from reporting.dataclasses import table_elements


class CountryTableManager(MontrekTableManager):
    repository_class = CountryRepository

    @property
    def table_elements(self) -> tuple:
        return (
            table_elements.LinkTextTableElement(
                name="Country Name",
                url="country_details",
                kwargs={"pk": "id"},
                text="country_name",
                hover_text="View Country",
            ),
            table_elements.StringTableElement(
                name="Country Code",
                attr="country_code",
            ),
        )


class CountryDetailsManager(MontrekDetailsManager):
    repository_class = CountryRepository

    @property
    def table_elements(self) -> tuple:
        return (
            table_elements.StringTableElement(
                name="Name",
                attr="country_name",
            ),
            table_elements.StringTableElement(
                name="Official Name",
                attr="country_official_name",
            ),
            table_elements.StringTableElement(
                name="Code",
                attr="country_code",
            ),
            table_elements.LinkTextTableElement(
                url="currency",
                name="Currency",
                text="ccy_code",
                hover_text="View Currency",
                kwargs={"filter": "ccy_code"},
            ),
            table_elements.ImageTableElement(
                name="Flag",
                attr="country_flag",
            ),
            table_elements.FloatTableElement(
                name="Latitude",
                attr="country_lat",
            ),
            table_elements.FloatTableElement(
                name="Longitude",
                attr="country_long",
            ),
            table_elements.StringTableElement(
                name="Capital",
                attr="country_capital",
            ),
            table_elements.StringTableElement(
                name="Region",
                attr="country_region",
            ),
            table_elements.StringTableElement(
                name="Subregion",
                attr="country_subregion",
            ),
            table_elements.StringTableElement(
                name="Continent",
                attr="country_continent",
            ),
            table_elements.IntTableElement(
                name="Area",
                attr="country_area",
            ),
            table_elements.IntTableElement(
                name="Population",
                attr="country_population",
            ),
            table_elements.BooleanTableElement(
                name="UN Member",
                attr="country_un_member",
            ),
            table_elements.StringTableElement(
                name="Postal Code Format",
                attr="country_postal_code_format",
            ),
            table_elements.StringTableElement(
                name="Postal Code Regex",
                attr="country_postal_code_regex",
            ),
        )


class CountryManager(MontrekManager):
    repository_class = CountryRepository
    request_manager = CountryRequestManager()

    def write_countries_to_db(self):
        countries_json = self.request_manager.get_countries_as_json()
        countries_df = self._countries_json_to_df(countries_json)
        self.repository.create_objects_from_data_frame(countries_df)

    def _countries_json_to_df(self, countries_json: list) -> pd.DataFrame:
        return pd.DataFrame(countries_json)


class RestCountriesManager(CountryManager):
    request_manager = RestCountriesRequestManager()

    def _countries_json_to_df(self, countries_json: list) -> pd.DataFrame:
        countries_df = pd.read_json(json.dumps(countries_json))
        countries_df["link_country_currency"] = self._create_currencies(
            countries_df["currencies"]
        )
        countries_df["country_name"] = countries_df["name"].apply(lambda x: x["common"])
        countries_df["country_official_name"] = countries_df["name"].apply(
            lambda x: x["official"]
        )
        countries_df["comment"] = f"Uploaded via {self.request_manager.base_url}"
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
            "cca2": "country_code",
            "capital": "country_capital",
            "unMember": "country_un_member",
            "region": "country_region",
            "subregion": "country_subregion",
            "area": "country_area",
            "population": "country_population",
        }
        countries_df = countries_df.rename(columns=rename_columns)
        return countries_df.loc[
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
