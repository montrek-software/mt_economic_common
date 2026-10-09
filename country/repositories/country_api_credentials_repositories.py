from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_economic_common.country.models.country_api_credentials_sat_models import (
    CountryApiCredentialsSatellite,
)
from mt_economic_common.country.models.country_api_credentials_hub_models import (
    CountryApiCredentialsHub,
)


class CountryApiCredentialsRepository(MontrekRepository):
    hub_class = CountryApiCredentialsHub

    def set_annotations(self):
        self.add_satellite_fields_annotations(
            CountryApiCredentialsSatellite, ["api_type", "token"]
        )
