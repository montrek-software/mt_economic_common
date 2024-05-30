import datetime
import factory


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
    class Meta:
        model = "country.CountryOecdTSSatellite"

    hub_entity = factory.SubFactory(CountryHubFactory)
    year = factory.Sequence(lambda n: 2000 + n)
    annual_fx_average = 1.0
    value_date = factory.LazyAttribute(lambda obj: datetime.date(obj.year, 1, 1))
