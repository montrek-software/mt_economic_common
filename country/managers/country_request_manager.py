from mt_economic_common.country.dataclasses.api_types import CountryApiTypeEnum
from mt_economic_common.country.repositories.country_api_credentials_repositories import (
    CountryApiCredentialsRepository,
)
from requesting.managers.authenticator_managers import RequestBearerAuthenticator
from requesting.managers.request_manager import RequestJsonManager


class RestCountriesRequestBearerAuthenticator(RequestBearerAuthenticator):
    def get_credentials(self):
        credentials = (
            CountryApiCredentialsRepository()
            .receive()
            .filter(api_type=CountryApiTypeEnum.REST_COUNTRIES.value.name)
            .first()
        )
        return {"token": credentials.token if credentials else None}


class RestCountriesRequestManager(RequestJsonManager):
    """
    Request manager for the REST Countries v5 API.

    The API wraps the countries in a paginated envelope
    (``{"data": {"objects": [...], "meta": {...}}}``); get_response walks through
    all pages and returns the plain list of country objects.
    """

    authenticator_class = RestCountriesRequestBearerAuthenticator
    base_url = "https://api.restcountries.com/countries/v5"
    page_size = 100
    response_fields = [
        "names.common",
        "names.official",
        "codes.alpha_2",
        "codes.alpha_3",
        "coordinates",
        "capitals",
        "postal_code",
        "links.google_maps",
        "links.open_street_maps",
        "flag.url_png",
        "classification.un_member",
        "currencies",
        "continents",
        "region",
        "subregion",
        "area.kilometers",
        "population",
    ]

    def get_response(self, endpoint: str) -> list:
        if not self.authenticator.credentials["token"]:
            self.status_code = 0
            self.message = "No API key for REST Countries configured"
            return []
        countries: list = []
        offset = 0
        while True:
            self.request_kwargs = {
                "response_fields": ",".join(self.response_fields),
                "limit": self.page_size,
                "offset": offset,
            }
            response = super().get_response(endpoint)
            if self.status_code != 200:
                return []
            data = response.get("data") if isinstance(response, dict) else None
            if not isinstance(data, dict) or "objects" not in data:
                self.status_code = 0
                self.message = "Unexpected response format from REST Countries API"
                return []
            objects = data["objects"]
            countries.extend(objects)
            if not objects or not data.get("meta", {}).get("more", False):
                return countries
            offset += len(objects)
