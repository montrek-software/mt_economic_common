from mt_economic_common.country.dataclasses.api_types import CountryApiTypeEnum
from mt_economic_common.country.repositories.country_api_credentials_repositories import (
    CountryApiCredentialsRepository,
)
from requesting.managers.authenticator_managers import RequestBearerAuthenticator
from requesting.managers.request_manager import RequestJsonManager


class RestCountriesRequestBearerAuthenticator(RequestBearerAuthenticator):
    def get_credentials(self):
        token = (
            CountryApiCredentialsRepository()
            .receive()
            .get(api_type=CountryApiTypeEnum.REST_COUNTRIES.value.name)
            .token
        )
        return {"token": token}


class RestCountriesRequestManager(RequestJsonManager):
    authenticator_class = RestCountriesRequestBearerAuthenticator
    base_url = "https://api.restcountries.com/countries/v5/"
    request_kwargs = {
        "fields": ",".join(
            [
                "cca2",
                "name",
                "cca3",
                "latlng",
                "capital",
                "postalCode",
                "maps",
                "flags",
                "unMember",
                "currencies",
            ]
        )
    }


class RestCountriesLocalityRequestManager(RestCountriesRequestManager):
    request_kwargs = {
        "fields": ",".join(
            [
                "cca2",
                "continents",
                "unMember",
                "region",
                "subregion",
                "area",
                "population",
                "currencies",
            ]
        )
    }
