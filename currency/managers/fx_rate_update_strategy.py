from typing import List, Dict
import pandas as pd
from django.utils import timezone
import yfinance as yf
from baseclasses.dataclasses.montrek_message import MontrekMessage, MontrekMessageError


class FxUpdateStrategyBase:
    def __init__(self):
        self.messages: list[MontrekMessage] = []

    def get_fx_rates_from_source(
        self,
        currency_code_list: List[str],
        value_date: timezone.datetime,
    ) -> Dict[str, float]:
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement _get_fx_rates_from_source()"
        )


class YahooFxRateUpdateStrategy(FxUpdateStrategyBase):
    def get_fx_rates_from_source(
        self,
        currency_code_list: List[str],
        value_date: timezone.datetime,
    ) -> Dict[str, float]:
        fx_rates = {}
        for ccy in currency_code_list:
            if ccy == "EUR":
                fx_rates[ccy] = 1.0
                continue
            pair_code = f"{ccy}EUR=X"
            data = yf.Ticker(pair_code)
            date_str = value_date.strftime("%Y-%m-%d")
            hist = data.history(
                start=date_str,
                end=(value_date + timezone.timedelta(days=1)).strftime("%Y-%m-%d"),
                period="1d",
            )
            fx_rates[ccy] = self.handle_hist_data_and_return_fx_rates(
                hist, pair_code, date_str
            )
        return fx_rates

    def handle_hist_data_and_return_fx_rates(
        self, hist: pd.DataFrame, pair_code: str, date_str: str
    ) -> float | None:
        if hist.empty:
            self.messages.append(
                MontrekMessageError(
                    f"YahooFxRateUpdateStrategy: {pair_code} has no data for {date_str}"
                )
            )
            return None
        return hist["Close"].iloc[-1]
