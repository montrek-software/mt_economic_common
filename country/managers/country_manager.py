import pandas as pd
import numpy as np
import json
from mt_economic_common.country.repositories.country_repository import CountryRepository
from mt_economic_common.country.managers.country_request_manager import (
    CountryRequestManager,
    RestCountriesRequestManager,
)


class CountryManager:
    repository_class = CountryRepository
    request_manager = CountryRequestManager()

    def __init__(self, session_data: dict):
        self.repository = self.repository_class(session_data=session_data)

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
            ]
            + list(rename_columns.values()),
        ]

    def _get_json_field(self, json_obj: dict | None, field_name: str):
        if pd.isnull(json_obj):
            return None
        return json_obj.get(field_name, None)
