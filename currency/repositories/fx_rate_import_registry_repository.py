from data_import.base.repositories.registry_repositories import RegistryRepositoryABC

from mt_economic_common.currency.constants import FX_SOURCE_KEY, FX_VALUE_DATE_KEY
from mt_economic_common.currency.models import (
    FxRateImportRegistryHub,
    FxRateImportRegistrySatellite,
)


class FxRateImportRegistryRepository(RegistryRepositoryABC):
    hub_class = FxRateImportRegistryHub
    registry_satellite = FxRateImportRegistrySatellite
    registry_fields = [
        *RegistryRepositoryABC.registry_fields,
        FX_SOURCE_KEY,
        FX_VALUE_DATE_KEY,
    ]
