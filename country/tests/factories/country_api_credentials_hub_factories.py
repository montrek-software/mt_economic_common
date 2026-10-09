import factory

from baseclasses.tests.factories.baseclass_factories import ValueDateListFactory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekHubValueDateFactory,
    MontrekHubFactory,
)
from mt_economic_common.country.models.country_api_credentials_hub_models import (
    CountryApiCredentialsHub,
)
from mt_economic_common.country.models.country_api_credentials_hub_models import (
    CountryApiCredentialsHubValueDate,
)


class CountryApiCredentialsHubFactory(MontrekHubFactory):
    class Meta:
        model = CountryApiCredentialsHub


class CountryApiCredentialsHubValueDateFactory(MontrekHubValueDateFactory):
    class Meta:
        model = CountryApiCredentialsHubValueDate

    hub = factory.SubFactory(CountryApiCredentialsHubFactory)
    value_date_list = factory.SubFactory(ValueDateListFactory)
