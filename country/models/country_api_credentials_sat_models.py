from baseclasses.models import MontrekSatelliteABC
from django.db import models
from encrypted_fields import EncryptedCharField
from mt_economic_common.country.dataclasses.api_types import CountryApiTypeEnum

from mt_economic_common.country.models.country_api_credentials_hub_models import (
    CountryApiCredentialsHub,
)


class CountryApiCredentialsSatellite(MontrekSatelliteABC):
    hub_entity = models.ForeignKey(CountryApiCredentialsHub, on_delete=models.CASCADE)

    api_type = models.CharField(choices=CountryApiTypeEnum.to_list())
    token = EncryptedCharField(null=True, blank=True)

    identifier_fields = ["hub_entity_id"]
