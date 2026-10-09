import factory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekSatelliteFactory,
)

from mt_economic_common.country.tests.factories.country_api_credentials_hub_factories import (
    CountryApiCredentialsHubFactory,
)
from mt_economic_common.country.models.country_api_credentials_sat_models import (
    CountryApiCredentialsSatellite,
)


class CountryApiCredentialsSatelliteFactory(MontrekSatelliteFactory):
    class Meta:
        model = CountryApiCredentialsSatellite

    hub_entity = factory.SubFactory(CountryApiCredentialsHubFactory)
