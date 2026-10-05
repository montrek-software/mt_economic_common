import datetime
from decimal import Decimal
from typing import Any

from django.test import TestCase
from requesting.managers.request_manager import RequestJsonManager
from testing.decorators.add_logged_in_user import add_logged_in_user

from mt_economic_common.currency.constants import FX_VALUE_DATE_KEY
from mt_economic_common.currency.managers.fx_rate_import_processors import (
    FrankfurterFxRateImportProcessor,
)
from mt_economic_common.currency.managers.fx_rate_request_managers import (
    FrankfurterRequestManager,
)
from mt_economic_common.currency.managers.fx_rate_sources import FxRateSource
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)
from mt_economic_common.currency.tests.factories.currency_factories import (
    CurrencyStaticSatelliteFactory,
)

TEST_VALUE_DATE = datetime.date(2026, 10, 2)
TEST_RESPONSE = {
    "amount": 1.0,
    "base": "EUR",
    "date": "2026-10-02",
    "rates": {"GBP": 0.85033, "USD": 1.1225},
}


class MockFrankfurterRequestManager(RequestJsonManager):
    response: dict[str, Any] = TEST_RESPONSE
    response_status_code = 200
    requested_endpoints: list[str] = []

    def get_response(self, endpoint: str) -> dict[str, Any]:
        self.requested_endpoints.append(endpoint)
        self.status_code = self.response_status_code
        if self.status_code != 200:
            self.message = "404 Client Error: NOT FOUND"
            return {}
        self.message = "OK"
        return self.response


class MockFailingFrankfurterRequestManager(MockFrankfurterRequestManager):
    response_status_code = 404


class MockFrankfurterProcessor(FrankfurterFxRateImportProcessor):
    request_manager_class = MockFrankfurterRequestManager


class TestFrankfurterRequestManager(TestCase):
    def test_endpoint_url(self):
        self.assertEqual(
            FrankfurterRequestManager.get_endpoint_url("2026-10-02?symbols=USD"),
            "https://api.frankfurter.app/2026-10-02?symbols=USD",
        )


class TestFrankfurterFxRateImportProcessor(TestCase):
    @add_logged_in_user
    def setUp(self):
        self.session_data = {"user_id": self.user.id}
        MockFrankfurterRequestManager.requested_endpoints = []

    def run_import(
        self,
        currency_codes: list[str],
        request_manager_class: type[MockFrankfurterRequestManager],
        value_date: datetime.date = TEST_VALUE_DATE,
    ) -> tuple[MockFrankfurterProcessor, bool]:
        for ccy_code in currency_codes:
            CurrencyStaticSatelliteFactory(ccy_code=ccy_code)
        processor = MockFrankfurterProcessor(self.session_data, {})
        processor.request_manager_class = request_manager_class
        processor.set_pipeline_data({FX_VALUE_DATE_KEY: value_date.isoformat()})
        result = (
            processor.pre_check() and processor.process() and processor.post_check()
        )
        return processor, result

    def get_fx_rates(self) -> dict[str, Decimal]:
        return {
            obj.ccy_code: obj.fx_rate
            for obj in CurrencyRepository(self.session_data).receive()
        }

    def test_source_is_registered(self):
        self.assertEqual(
            FxRateSource.from_label("frankfurter").value.processor_class,
            FrankfurterFxRateImportProcessor,
        )

    def test_rates_are_converted_to_eur_per_unit(self):
        processor, result = self.run_import(
            ["EUR", "GBP", "USD"], MockFrankfurterRequestManager
        )

        self.assertTrue(result)
        self.assertEqual(
            self.get_fx_rates(),
            {
                "EUR": Decimal("1.0000000000"),
                "GBP": Decimal("1.1760140181"),
                "USD": Decimal("0.8908685969"),
            },
        )
        self.assertEqual(processor.message, "Imported 3 FX rates for 2026-10-02")

    def test_base_currency_is_not_requested(self):
        self.run_import(["EUR", "GBP", "USD"], MockFrankfurterRequestManager)

        self.assertEqual(
            MockFrankfurterRequestManager.requested_endpoints,
            ["2026-10-02?symbols=GBP,USD"],
        )

    def test_only_base_currency_needs_no_request(self):
        _, result = self.run_import(["EUR"], MockFrankfurterRequestManager)

        self.assertTrue(result)
        self.assertEqual(MockFrankfurterRequestManager.requested_endpoints, [])

    def test_unsupported_currencies_are_reported(self):
        processor, result = self.run_import(
            ["GBP", "USD", "XAF"], MockFrankfurterRequestManager
        )

        self.assertTrue(result)
        self.assertEqual(
            processor.message,
            "Imported 2 FX rates for 2026-10-02; no FX rate for XAF",
        )

    def test_earlier_fixing_is_noted(self):
        processor, result = self.run_import(
            ["GBP", "USD"],
            MockFrankfurterRequestManager,
            value_date=datetime.date(2026, 10, 3),
        )

        self.assertTrue(result)
        self.assertEqual(
            processor.message,
            "Imported 2 FX rates for 2026-10-03; ECB fixing of 2026-10-02 used",
        )
        value_dates = {
            obj.value_date for obj in CurrencyRepository(self.session_data).receive()
        }
        self.assertEqual(value_dates, {datetime.date(2026, 10, 3)})

    def test_failed_request_fails_import(self):
        processor, result = self.run_import(
            ["GBP", "USD"], MockFailingFrankfurterRequestManager
        )

        self.assertFalse(result)
        self.assertEqual(
            processor.message,
            "Frankfurter request for 2026-10-02 failed: 404 Client Error: NOT FOUND",
        )
