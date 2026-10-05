from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)
from reporting.dataclasses.table_elements import (
    LinkTableElement,
    StringTableElement,
)
from mt_economic_common.currency.table_elements import FxRateTableElement
from reporting.managers.montrek_details_manager import MontrekDetailsManager
from reporting.managers.montrek_table_manager import MontrekTableManager


class CurrencyManager(MontrekTableManager):
    repository_class = CurrencyRepository

    @property
    def table_elements(self) -> tuple:
        return (
            StringTableElement(name="Name", attr="ccy_name"),
            StringTableElement(name="Code", attr="ccy_code"),
            StringTableElement(name="Symbol", attr="ccy_symbol"),
            FxRateTableElement(name="FX Rate", attr="fx_rate"),
            LinkTableElement(
                name="Link",
                url="currency_details",
                kwargs={"pk": "hub_entity_id"},
                icon="chevron-right",
                hover_text="Goto Currency",
            ),
        )


class CurrencyDetailsManager(MontrekDetailsManager):
    repository_class = CurrencyRepository

    @property
    def table_elements(self) -> tuple:
        return (
            StringTableElement(name="Name", attr="ccy_name"),
            StringTableElement(name="Code", attr="ccy_code"),
            StringTableElement(name="Symbol", attr="ccy_symbol"),
            FxRateTableElement(name="FX Rate", attr="fx_rate"),
        )
