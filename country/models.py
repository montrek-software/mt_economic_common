from contextlib import nullcontext
from django.db import models
from baseclasses import models as baseclass_models


class CountryHub(baseclass_models.MontrekHubABC):
    pass


class CountryStaticSatellite(baseclass_models.MontrekSatelliteABC):
    hub_entity = models.ForeignKey(CountryHub, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=3)
    country_name = models.CharField(max_length=255, null=True)
    country_official_name = models.CharField(max_length=255, null=True)
    country_capital = models.CharField(max_length=100, null=True)
    country_un_member = models.BooleanField(default=False, null=True)
    country_region = models.CharField(max_length=100, null=True)
    country_subregion = models.CharField(max_length=100, null=True)
    country_lat = models.FloatField(null=True)
    country_long = models.FloatField(null=True)
    country_area = models.FloatField(null=True)
    country_population = models.BigIntegerField(null=True)
    country_continent = models.CharField(max_length=100, null=True)
    country_flag = models.CharField(max_length=255, null=True)
    country_postal_code_format = models.CharField(max_length=255, null=True)
    country_postal_code_regex = models.CharField(max_length=255, null=True)
    country_google_maps_url = models.CharField(max_length=255, null=True)
    identifier_fields = ["country_code"]

    def __str__(self):
        return self.country_name

    @classmethod
    def exclude_from_hash_value(cls) -> list[str]:
        exclude_fields = super().exclude_from_hash_value()
        exclude_fields.append("country_flag")
        return exclude_fields
