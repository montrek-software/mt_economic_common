import pandas as pd
from django.test import TestCase
from django.utils import timezone
from mt_economic_common.currency.managers.fx_rate_update_strategy import (
    YahooFxRateUpdateStrategy,
    FxUpdateStrategyBase,
)
from baseclasses.utils import montrek_time

TEST_CURRENCY_CODES = ["USD", "EUR", "GBP"]


class FxRateUpdateStrategyTestClass(FxUpdateStrategyBase):
    def get_fx_rates_from_source(
        self,
        currency_code_list: list[str],
        value_date: timezone.datetime,
    ) -> dict[str, float]:
        return {ccy: 1.0 for ccy in currency_code_list}


class TestFxRateUpdateStrategy(TestCase):
    def setUp(self):
        self.test_time = montrek_time(2023, 11, 28)

    def test_get_update_fx_rates_not_implemented(self):
        with self.assertRaises(NotImplementedError) as error:
            FxUpdateStrategyBase().get_fx_rates_from_source(
                TEST_CURRENCY_CODES, self.test_time
            )
        self.assertEqual(
            str(error.exception),
            "FxUpdateStrategyBase must implement _get_fx_rates_from_source()",
        )

    def test_right_currencies(self):
        strategy = FxRateUpdateStrategyTestClass()
        fx_rates = strategy.get_fx_rates_from_source(
            TEST_CURRENCY_CODES, self.test_time
        )
        expectd_fx_rates = {ccy: 1.0 for ccy in TEST_CURRENCY_CODES}
        self.assertEqual(fx_rates, expectd_fx_rates)


class TestYahooFxRateUpdateStrategy(TestCase):
    def test_get_fx_rates_from_source(self):
        test_time = timezone.datetime(2023, 11, 28)
        strategy = YahooFxRateUpdateStrategy()
        test_fx_rates = strategy.get_fx_rates_from_source(
            TEST_CURRENCY_CODES, test_time
        )
        expected_rates = {"USD": 0.9125, "EUR": 1.0, "GBP": 1.1529}
        for ccy, fx_rate in test_fx_rates.items():
            self.assertAlmostEqual(
                fx_rate,
                expected_rates[ccy],
                places=4,
            )

    def test_receive_no_data_message(self):
        strategy = YahooFxRateUpdateStrategy()
        strategy.handle_hist_data_and_return_fx_rates(pd.DataFrame(), "bli", "blubb")
        self.assertEqual(len(strategy.messages), 1)
        self.assertEqual(
            strategy.messages[0].message,
            "YahooFxRateUpdateStrategy: bli has no data for blubb",
        )
        test_result = strategy.handle_hist_data_and_return_fx_rates(
            pd.DataFrame({"Close": [1.2]}), "bli", "blubb"
        )
        self.assertEqual(test_result, 1.2)
