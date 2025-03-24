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
from mt_economic_common.sdmx_api.managers.sdmx_request_manager import (
    OecdSdmxRequestManager,
)
from reporting.dataclasses import table_elements as te
from reporting.managers.montrek_table_manager import MontrekTableManager


class CountryOecdManager(MontrekManager):
    repository_class = CountryOecdRepository


class CountryOecdAnnualFxUploadManager(ApiDataImportManager):
    registry_repository_class = CountryApiUploadRegistryRepository
    request_manager_class = OecdSdmxRequestManager
    processor_class = OecdAnnualFxUploadProcessor
    endpoint = "OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE4,/A....EXC_A.......?startPeriod=2000&dimensionAtObservation=AllDimensions"


class CountryOecdInflationUploadManager(ApiDataImportManager):
    registry_repository_class = CountryApiUploadRegistryRepository
    request_manager_class = OecdSdmxRequestManager
    processor_class = OecdInflationUploadProcessor
    endpoint = (
        "OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL,1.0/.A.N.CPI.IX._T.N.?startPeriod=2000"
    )


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
