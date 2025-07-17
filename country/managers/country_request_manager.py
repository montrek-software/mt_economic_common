from requesting.managers.request_manager import RequestJsonManager


class RestCountriesRequestManager(RequestJsonManager):
    base_url = "https://restcountries.com/v3.1/"
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
