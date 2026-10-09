from reporting.dataclasses import table_elements as te
from reporting.managers.montrek_table_manager import MontrekTableManager
from reporting.managers.montrek_details_manager import MontrekDetailsManager
from mt_economic_common.country.repositories.country_api_credentials_repositories import (
    CountryApiCredentialsRepository,
)


class CommonTableElementsMixin:
    @property
    def table_elements(self):
        return [
            te.StringTableElement(name="API Type", attr="api_type"),
            te.SecretStringTableElement(name="Token", attr="token"),
            te.LinkTableElement(
                name="Edit",
                url="country_api_credentials_update",
                icon="edit",
                kwargs={"pk": "id"},
                hover_text="Update Country Api Credentials",
            ),
            te.LinkTableElement(
                name="Delete",
                url="country_api_credentials_delete",
                icon="trash",
                kwargs={"pk": "id"},
                hover_text="Delete Country Api Credentials",
            ),
        ]


class CountryApiCredentialsTableManager(CommonTableElementsMixin, MontrekTableManager):
    repository_class = CountryApiCredentialsRepository

    @property
    def table_elements(self):
        table_elements = [
            te.LinkTextTableElement(
                name="Details",
                url="country_api_credentials_details",
                kwargs={"pk": "hub_id"},
                text="hub_entity_id",
                hover_text="View Country Api Credentials Details",
            ),
        ]
        table_elements += super().table_elements
        return table_elements


class CountryApiCredentialsDetailsManager(
    CommonTableElementsMixin, MontrekDetailsManager
):
    repository_class = CountryApiCredentialsRepository

    @property
    def table_elements(self):
        table_elements = [
            te.StringTableElement(name="hub", attr="hub_entity_id"),
        ]
        table_elements += super().table_elements
        return table_elements
