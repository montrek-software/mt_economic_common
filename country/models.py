from contextlib import nullcontext
from django.db import models
from baseclasses import models as baseclass_models


class CountryHub(baseclass_models.MontrekHubABC):
    link_country_currency = models.ManyToManyField(
        "currency.CurrencyHub",
        related_name="link_currency_country",
        through="LinkCountryCurrency",
    )


class CountryStaticSatellite(baseclass_models.MontrekSatelliteABC):
    hub_entity = models.ForeignKey(CountryHub, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=3)
    country_code_2 = models.CharField(max_length=2, null=True, blank=True)
    country_name = models.CharField(max_length=255, null=True)
    country_official_name = models.CharField(max_length=255, null=True, blank=True)
    country_capital = models.CharField(max_length=100, null=True, blank=True)
    country_un_member = models.BooleanField(default=False, null=True, blank=True)
    country_region = models.CharField(max_length=100, null=True, blank=True)
    country_subregion = models.CharField(max_length=100, null=True, blank=True)
    country_lat = models.FloatField(null=True, blank=True)
    country_long = models.FloatField(null=True, blank=True)
    country_area = models.FloatField(null=True, blank=True)
    country_population = models.BigIntegerField(null=True, blank=True)
    country_continent = models.CharField(max_length=100, null=True, blank=True)
    country_flag = models.CharField(max_length=255, null=True, blank=True)
    country_postal_code_format = models.CharField(max_length=255, null=True, blank=True)
    country_postal_code_regex = models.CharField(max_length=255, null=True, blank=True)
    country_google_maps_url = models.CharField(max_length=255, null=True, blank=True)
    country_open_street_map_url = models.CharField(
        max_length=255, null=True, blank=True
    )
    identifier_fields = ["country_code"]

    def __str__(self):
        return self.country_name


class LinkCountryCurrency(baseclass_models.MontrekManyToManyLinkABC):
    hub_in = models.ForeignKey(
        "country.CountryHub",
        on_delete=models.CASCADE,
    )
    hub_out = models.ForeignKey("currency.CurrencyHub", on_delete=models.CASCADE)
