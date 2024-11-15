from django.utils import timezone
from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_economic_common.country.models import (
    CountryHub,
    CountryStaticSatellite,
    LinkCountryCurrency,
    CountryApiUploadRegistryHub,
    CountryApiUploadRegistryStaticSatellite,
)
from mt_economic_common.currency.models import CurrencyStaticSatellite
from api_upload.repositories.api_upload_registry_repository import (
    ApiUploadRepositoryABC,
)


class CountryRepository(MontrekRepository):
    hub_class = CountryHub
    default_order_fields = ("country_name",)

    def set_annotations(self):
        self.add_satellite_fields_annotations(
            CountryStaticSatellite,
            [
                "country_name",
                "country_official_name",
                "country_code",
                "country_code_2",
                "country_flag",
                "country_lat",
                "country_long",
                "country_un_member",
                "country_region",
                "country_subregion",
                "country_continent",
                "country_capital",
                "country_area",
                "country_population",
                "country_continent",
                "country_postal_code_format",
                "country_postal_code_regex",
                "country_google_maps_url",
                "country_open_street_map_url",
            ],
        )
        self.add_linked_satellites_field_annotations(
            CurrencyStaticSatellite,
            LinkCountryCurrency,
            [
                "ccy_code",
            ],
        )


class CountryApiUploadRegistryRepository(ApiUploadRepositoryABC):
    hub_class = CountryApiUploadRegistryHub
    static_satellite_class = CountryApiUploadRegistryStaticSatellite
