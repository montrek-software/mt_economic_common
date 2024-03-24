import pandas as pd
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
        countries_df = pd.DataFrame(countries_json)
        countries_df["country_name"] = countries_df["name"].apply(lambda x: x["common"])
        countries_df["country_code"] = countries_df["cca2"]
        return countries_df.loc[:, ["country_name", "country_code"]]
