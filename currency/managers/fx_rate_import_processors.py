import datetime
from typing import Any

import pandas as pd
from data_import.base.managers.processor_base import ProcessorBaseABC
from data_import.types import ImportDataType

from mt_economic_common.currency.constants import FX_VALUE_DATE_KEY
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)


class FxRateImportProcessorABC(ProcessorBaseABC):
    """Imports the FX rates of all currencies for one value date.

    Subclasses only fetch the rates from their source. FX rates are stored as the
    value of one unit of the currency in EUR.
    """

    def __init__(self, session_data: dict[str, Any], import_data: ImportDataType):
        super().__init__(session_data, import_data)
        self.repository = CurrencyRepository(session_data)
        self.value_date = datetime.date.min
        self.currency_hub_ids: dict[str, int] = {}
        self.fx_rates: dict[str, float] = {}

    def pre_check(self) -> bool:
        self.value_date = datetime.date.fromisoformat(
            self.pipeline_data[FX_VALUE_DATE_KEY]
        )
        self.currency_hub_ids = {
            obj.ccy_code: obj.hub.id for obj in self.repository.receive()
        }
        if not self.currency_hub_ids:
            self.set_message("No currencies found to import FX rates for")
            return False
        return True

    def process(self) -> bool:
        self.fx_rates = self.get_fx_rates(list(self.currency_hub_ids), self.value_date)
        if not self.fx_rates:
            self.set_message(f"No FX rates received for {self.value_date}")
            return False
        input_data = pd.DataFrame(
            {
                "hub_entity_id": [
                    self.currency_hub_ids[ccy_code] for ccy_code in self.fx_rates
                ],
                "fx_rate": list(self.fx_rates.values()),
                "value_date": self.value_date,
            }
        )
        self.repository.create_by_data_frame(input_data)
        return True

    def post_check(self) -> bool:
        message = f"Imported {len(self.fx_rates)} FX rates for {self.value_date}"
        missing_codes = sorted(set(self.currency_hub_ids) - set(self.fx_rates))
        if missing_codes:
            message += f"; no FX rate for {', '.join(missing_codes)}"
        self.set_message(message)
        return True

    def get_fx_rates(
        self, currency_codes: list[str], value_date: datetime.date
    ) -> dict[str, float]:
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement get_fx_rates()"
        )


class DummyFxRateImportProcessor(FxRateImportProcessorABC):
    """Sets every FX rate to 1, for testing without an external API."""

    def get_fx_rates(
        self, currency_codes: list[str], value_date: datetime.date
    ) -> dict[str, float]:
        return dict.fromkeys(currency_codes, 1.0)
