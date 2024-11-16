import pandas as pd
from baseclasses.managers.montrek_manager import MontrekManager
from django.utils import timezone
from mt_economic_common.currency.managers.fx_rate_update_strategy import (
    FxUpdateStrategyBase,
    YahooFxRateUpdateStrategy,
)
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)
from reporting.dataclasses.table_elements import (
    FloatTableElement,
    LinkTableElement,
    StringTableElement,
)
from reporting.managers.montrek_details_manager import MontrekDetailsManager
from reporting.managers.montrek_table_manager import MontrekTableManager


class FxUploadManager(MontrekManager):
    repository_class = CurrencyRepository
    fx_update_strategy_class: type[FxUpdateStrategyBase] = FxUpdateStrategyBase

    def __init__(self, session_data: dict):
        super().__init__(session_data=session_data)
        self.fx_update_strategy = self.fx_update_strategy_class()

    def update_fx_rates(self, value_date: timezone.datetime):
        currency_code_list = self._get_all_currency_codes_from_db()
        fx_rates = self.fx_update_strategy.get_fx_rates_from_source(
            currency_code_list, value_date
        )
        self._add_fx_rates_to_db(fx_rates, value_date)

    def _get_all_currency_codes_from_db(self) -> list[str]:
        return [obj.ccy_code for obj in self.repository.receive()]

    def _add_fx_rates_to_db(
        self, fx_rates: dict[str, float], value_date: timezone.datetime
    ):
        input_data = pd.DataFrame(
            {
                "ccy_code": list(fx_rates.keys()),
                "fx_rate": list(fx_rates.values()),
                "value_date": [value_date] * len(fx_rates.keys()),
            }
        )
        self.repository.create_by_data_frame(input_data)


class YahooFxUploadManager(FxUploadManager):
    fx_update_strategy_class: type[FxUpdateStrategyBase] = YahooFxRateUpdateStrategy


class CurrencyManager(MontrekTableManager):
    repository_class = CurrencyRepository

    @property
    def table_elements(self) -> tuple:
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


class CurrencyDetailsManager(MontrekDetailsManager):
    repository_class = CurrencyRepository

    @property
    def table_elements(self) -> tuple:
        return (
            StringTableElement(name="Name", attr="ccy_name"),
            StringTableElement(name="Code", attr="ccy_code"),
            StringTableElement(name="Symbol", attr="ccy_symbol"),
            FloatTableElement(name="FX Rate", attr="fx_rate"),
        )
