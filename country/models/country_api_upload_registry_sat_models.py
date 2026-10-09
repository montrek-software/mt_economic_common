from data_import.api_import.models import ApiRegistrySatellite
from django.db import models

from mt_economic_common.country.models.country_api_upload_registry_hub_models import (
    CountryApiUploadRegistryHub,
)


class CountryApiUploadRegistryStaticSatellite(ApiRegistrySatellite):
    hub_entity = models.ForeignKey(
        CountryApiUploadRegistryHub, on_delete=models.CASCADE
    )
