from dataclasses import dataclass
from typing import ClassVar

from reporting.dataclasses.table_elements import FloatTableElement

FX_RATE_DECIMAL_PLACES = 6


@dataclass
class FxRateTableElement(FloatTableElement):
    """FX rates of weak currencies against EUR need more than three decimals."""

    _excel_decimal_places: ClassVar[int] = FX_RATE_DECIMAL_PLACES

    def _format_value(self, value) -> str:
        return self.shortener.shorten(value, FX_RATE_DECIMAL_PLACES)
