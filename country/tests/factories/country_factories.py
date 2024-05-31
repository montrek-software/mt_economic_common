import datetime
import factory
from api_upload.tests.factories import (
    ApiUploadRegistryHubFactory,
    ApiUploadRegistryStaticSatelliteFactory,
)


class CountryHubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "country.CountryHub"


class CountryStaticSatelliteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "country.CountryStaticSatellite"

    hub_entity = factory.SubFactory(CountryHubFactory)
    country_name = factory.Sequence(lambda n: f"country_name_{n}")
    country_code = factory.Sequence(lambda n: f"{n:03d}")


class CountryOecdTSSatelliteFactory(factory.django.DjangoModelFactory):
    hub_entity = factory.SubFactory(CountryHubFactory)
    year = factory.Sequence(lambda n: 2000 + n)
    value_date = factory.LazyAttribute(lambda obj: datetime.date(obj.year, 1, 1))


class CountryOecdFxAnnualTSSatelliteFactory(CountryOecdTSSatelliteFactory):
    class Meta:
        model = "country.CountryOecdFxAnnualTSSatellite"

    annual_fx_average = 1.0


class CountryOecdInflationTSSatelliteFactory(CountryOecdTSSatelliteFactory):
    class Meta:
        model = "country.CountryOecdInflationTSSatellite"

    inflation = 100.0


class CountryApiUploadRegistryHubFactory(ApiUploadRegistryHubFactory):
    class Meta:
        model = "country.CountryApiUploadRegistryHub"


class CountryApiUploadRegistryStaticSatelliteFactory(
    ApiUploadRegistryStaticSatelliteFactory
):
    class Meta:
        model = "country.CountryApiUploadRegistryStaticSatellite"

    hub_entity = factory.SubFactory(CountryApiUploadRegistryHubFactory)
