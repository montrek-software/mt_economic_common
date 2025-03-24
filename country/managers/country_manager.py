from data_import.api_import.managers.api_data_import_manager import ApiDataImportManager
from baseclasses.managers.montrek_manager import MontrekManager
from reporting.managers.montrek_table_manager import MontrekTableManager
from reporting.managers.montrek_details_manager import MontrekDetailsManager
from mt_economic_common.country.repositories.country_repository import (
    CountryRepository,
    CountryApiUploadRegistryRepository,
)
from mt_economic_common.country.managers.country_request_manager import (
    RestCountriesRequestManager,
)
from reporting.dataclasses import table_elements
from mt_economic_common.country.managers.country_upload_processors import (
    RestCountriesUploadProcessor,
)


class CountryManager(MontrekManager):
    repository_class = CountryRepository


class CountryTableManager(MontrekTableManager):
    repository_class = CountryRepository

    @property
    def table_elements(self) -> tuple:
        return (
            table_elements.LinkTextTableElement(
                name="Country Name",
                url="country_details",
                kwargs={"pk": "hub_id"},
                text="country_name",
                hover_text="View Country",
            ),
            table_elements.StringTableElement(
                name="Country Code",
                attr="country_code",
            ),
            table_elements.StringTableElement(
                name="Code2",
                attr="country_code_2",
            ),
            table_elements.StringTableElement(
                name="Region",
                attr="country_region",
            ),
            table_elements.StringTableElement(
                name="Subregion",
                attr="country_subregion",
            ),
            table_elements.StringTableElement(
                name="Continent",
                attr="country_continent",
            ),
            table_elements.IntTableElement(
                name="Area [km²]",
                attr="country_area",
            ),
            table_elements.IntTableElement(
                name="Population",
                attr="country_population",
            ),
        )


class CountryDetailsManager(MontrekDetailsManager):
    repository_class = CountryRepository

    @property
    def table_elements(self) -> tuple:
        return (
            table_elements.StringTableElement(
                name="Name",
                attr="country_name",
            ),
            table_elements.StringTableElement(
                name="Official Name",
                attr="country_official_name",
            ),
            table_elements.StringTableElement(
                name="Code",
                attr="country_code",
            ),
            table_elements.StringTableElement(
                name="Code2",
                attr="country_code_2",
            ),
            table_elements.LinkTextTableElement(
                url="currency",
                name="Currency",
                text="ccy_code",
                hover_text="View Currency",
                kwargs={"filter": "ccy_code"},
            ),
            table_elements.ImageTableElement(
                name="Flag",
                attr="country_flag",
            ),
            table_elements.FloatTableElement(
                name="Latitude",
                attr="country_lat",
            ),
            table_elements.FloatTableElement(
                name="Longitude",
                attr="country_long",
            ),
            table_elements.StringTableElement(
                name="Capital",
                attr="country_capital",
            ),
            table_elements.StringTableElement(
                name="Region",
                attr="country_region",
            ),
            table_elements.StringTableElement(
                name="Subregion",
                attr="country_subregion",
            ),
            table_elements.StringTableElement(
                name="Continent",
                attr="country_continent",
            ),
            table_elements.IntTableElement(
                name="Area",
                attr="country_area",
            ),
            table_elements.IntTableElement(
                name="Population",
                attr="country_population",
            ),
            table_elements.BooleanTableElement(
                name="UN Member",
                attr="country_un_member",
            ),
        )


class RestCountriesUploadManager(ApiDataImportManager):
    registry_repository_class = CountryApiUploadRegistryRepository
    request_manager_class = RestCountriesRequestManager
    processor_class = RestCountriesUploadProcessor
    endpoint = "all"


class CountryApiUploadRegistryManager(MontrekTableManager):
    repository_class = CountryApiUploadRegistryRepository

    @property
    def table_elements(self) -> tuple:
        return (
            table_elements.StringTableElement(
                name="URL",
                attr="url",
            ),
            table_elements.StringTableElement(
                name="Upload Status",
                attr="upload_status",
            ),
            table_elements.StringTableElement(
                name="Upload Message",
                attr="upload_message",
            ),
            table_elements.DateTimeTableElement(name="Created At", attr="created_at"),
            table_elements.StringTableElement(name="Created By", attr="created_by"),
        )
