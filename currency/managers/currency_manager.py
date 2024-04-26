from reporting.managers.montrek_table_manager import MontrekTableManager
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)
from reporting.dataclasses.table_elements import (
    StringTableElement,
    LinkTableElement,
    FloatTableElement,
)


class CurrencyManager(MontrekTableManager):
    repository_class = CurrencyRepository

    @property
    def table_elements(self) -> dict:
        return (
            StringTableElement(name="Name", attr="ccy_name"),
            StringTableElement(name="Code", attr="ccy_code"),
            StringTableElement(name="Symbol", attr="ccy_symbol"),
            FloatTableElement(name="FX Rate", attr="fx_rate"),
            LinkTableElement(
                name="Link",
                url="currency_details",
                kwargs={"pk": "id"},
                icon="chevron-right",
                hover_text="Goto Currency",
            ),
        )
