
import factory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekHubFactory,
    MontrekHubValueDateFactory,
    MontrekSatelliteFactory,
    MontrekTSSatelliteFactory,
)
from data_import.api_import.tests.factories.api_data_import_registry_factories import ApiDataImportRegistryBaseSatelliteFactory


class CountryHubFactory(MontrekHubFactory):
    class Meta:
        model = "country.CountryHub"


class CountryHubValueDateFactory(MontrekHubValueDateFactory):
    class Meta:
        model = "country.CountryHubValueDate"

    hub = factory.SubFactory(CountryHubFactory)


class CountryStaticSatelliteFactory(MontrekSatelliteFactory):
    class Meta:
        model = "country.CountryStaticSatellite"

    hub_entity = factory.SubFactory(CountryHubFactory)
    country_name = factory.Sequence(lambda n: f"country_name_{n}")
    country_code = factory.Sequence(lambda n: f"{n:03d}")


class CountryOecdTSSatelliteFactory(MontrekTSSatelliteFactory):
    hub_value_date = factory.SubFactory(CountryHubValueDateFactory)
    year = factory.Sequence(lambda n: 2000 + n)


class CountryOecdFxAnnualTSSatelliteFactory(CountryOecdTSSatelliteFactory):
    class Meta:
        model = "country.CountryOecdFxAnnualTSSatellite"

    annual_fx_average = 1.0


class CountryOecdInflationTSSatelliteFactory(CountryOecdTSSatelliteFactory):
    class Meta:
        model = "country.CountryOecdInflationTSSatellite"

    inflation = 100.0


class CountryApiUploadRegistryHubFactory(MontrekHubFactory):
    class Meta:
        model = "country.CountryApiUploadRegistryHub"


class CountryApiUploadRegistryStaticSatelliteFactory(
    ApiDataImportRegistryBaseSatelliteFactory
):
    class Meta:
        model = "country.CountryApiUploadRegistryStaticSatellite"

    hub_entity = factory.SubFactory(CountryApiUploadRegistryHubFactory)
