from reporting.managers.montrek_table_manager import MontrekTableManager
from reporting.managers.montrek_details_manager import MontrekDetailsManager
from mt_economic_common.credit_institution.repositories.credit_institution_repository import (
    CreditInstitutionRepository,
)
from reporting.dataclasses.table_elements import (
    StringTableElement,
    LinkTableElement,
    LinkTextTableElement,
)


class CreditInstitutionManager(MontrekTableManager):
    repository_class = CreditInstitutionRepository

    @property
    def table_elements(self) -> dict:
        return (
            StringTableElement(name="Name", attr="credit_institution_name"),
            LinkTableElement(
                name="Link",
                url="credit_institution_details",
                kwargs={"pk": "id"},
                icon="chevron-right",
                hover_text="Goto Credit Institution",
            ),
            StringTableElement(name="BIC", attr="credit_institution_bic"),
            StringTableElement(name="Upload Method", attr="account_upload_method"),
            LinkTextTableElement(
                name="Country",
                url="country_details",
                kwargs={"pk": "country_id"},
                text="country_name",
                hover_text="Goto Country",
            ),
        )


class CreditInstitutionDetailsManager(MontrekDetailsManager):
    repository_class = CreditInstitutionRepository

    @property
    def table_elements(self) -> tuple:
        return (
            StringTableElement(name="Name", attr="credit_institution_name"),
            StringTableElement(name="BIC", attr="credit_institution_bic"),
            StringTableElement(name="Upload Method", attr="account_upload_method"),
        )
