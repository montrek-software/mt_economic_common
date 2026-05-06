from baseclasses.managers.montrek_manager import MontrekManager
from data_import.api_import.managers.api_data_import_manager import ApiDataImportManager
from mt_economic_common.country.managers.country_upload_processors import (
    OecdAnnualFxUploadProcessor,
    OecdInflationUploadProcessor,
)
from mt_economic_common.country.repositories.country_oecd_repository import (
    CountryOecdApiRepository,
    CountryOecdRepository,
    CountryOecdTableRepository,
)
from mt_economic_common.country.repositories.country_repository import (
    CountryApiUploadRegistryRepository,
)
from reporting.dataclasses import table_elements as te
from reporting.managers.montrek_table_manager import MontrekTableManager


class CountryOecdManager(MontrekManager):
    repository_class = CountryOecdRepository


class CountryOecdAnnualFxUploadManager(ApiDataImportManager):
    registry_repository_class = CountryApiUploadRegistryRepository
    processor_class = OecdAnnualFxUploadProcessor


class CountryOecdInflationUploadManager(ApiDataImportManager):
    registry_repository_class = CountryApiUploadRegistryRepository
    processor_class = OecdInflationUploadProcessor


class YearTableElement(te.IntTableElement):
    def _format_value(self, value: int) -> str:
        return str(value)


class CountryOecdTableManager(MontrekTableManager):
    repository_class = CountryOecdTableRepository

    @property
    def table_elements(self) -> list:
        return [
            YearTableElement(name="Year", attr="year"),
            te.FloatTableElement(name="Annual FX Average", attr="annual_fx_average"),
            te.FloatTableElement(name="Inflation", attr="inflation"),
        ]


class CountryOecdDataApiManager(MontrekTableManager):
    repository_class = CountryOecdApiRepository

    @property
    def table_elements(self) -> list:
        return [
            te.StringTableElement(name="Country Code", attr="country_code_2"),
            YearTableElement(name="Year", attr="year"),
            te.FloatTableElement(name="Annual FX Average", attr="annual_fx_average"),
            te.FloatTableElement(name="Inflation", attr="inflation"),
        ]
