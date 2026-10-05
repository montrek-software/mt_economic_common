import factory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekHubFactory,
    MontrekSatelliteFactory,
    MontrekTSSatelliteFactory,
    MontrekHubValueDateFactory,
)


class CurrencyHubFactory(MontrekHubFactory):
    class Meta:
        model = "currency.CurrencyHub"


class CurrencyHubValueDateFactory(MontrekHubValueDateFactory):
    class Meta:
        model = "currency.CurrencyHubValueDate"

    hub = factory.SubFactory(CurrencyHubFactory)


class CurrencyStaticSatelliteFactory(MontrekSatelliteFactory):
    class Meta:
        model = "currency.CurrencyStaticSatellite"

    hub_entity = factory.SubFactory(CurrencyHubFactory)


class CurrencyTimeSeriesSatelliteFactory(MontrekTSSatelliteFactory):
    class Meta:
        model = "currency.CurrencyTimeSeriesSatellite"

    hub_value_date = factory.SubFactory(CurrencyHubValueDateFactory)


class FxRateImportRegistryHubFactory(MontrekHubFactory):
    class Meta:
        model = "currency.FxRateImportRegistryHub"


class FxRateImportRegistryHubValueDateFactory(MontrekHubValueDateFactory):
    class Meta:
        model = "currency.FxRateImportRegistryHubValueDate"

    hub = factory.SubFactory(FxRateImportRegistryHubFactory)


class FxRateImportRegistrySatelliteFactory(MontrekSatelliteFactory):
    class Meta:
        model = "currency.FxRateImportRegistrySatellite"

    hub_entity = factory.SubFactory(FxRateImportRegistryHubFactory)
    fx_source = "dummy"
