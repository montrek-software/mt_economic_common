from django.test import TestCase
from django.utils import timezone
from testing.decorators.add_logged_in_user import add_logged_in_user

from mt_economic_common.currency.managers.currency_manager import (
    FxUploadManager,
)
from mt_economic_common.currency.managers.fx_rate_update_strategy import (
    FxUpdateStrategyBase,
)
from mt_economic_common.currency.tests.factories.currency_factories import (
    CurrencyStaticSatelliteFactory,
)
from mt_economic_common.currency.tests.managers.test_fx_rate_update_strategy import (
    FxRateUpdateStrategyTestClass,
)

TEST_CURRENCY_CODES = ["USD", "EUR", "GBP"]


class MockFxUploadManager(FxUploadManager):
    fx_update_strategy_class: type[FxUpdateStrategyBase] = FxRateUpdateStrategyTestClass


class TestFxUploadManager(TestCase):
    @add_logged_in_user
    def setUp(self):
        self.session_data = {"user_id": self.user.id}
        for ccy in TEST_CURRENCY_CODES:
            CurrencyStaticSatelliteFactory(ccy_code=ccy)

    def test_update_fx_rates(self):
        manager = MockFxUploadManager(session_data=self.session_data)
        manager.update_fx_rates(value_date=timezone.now())
        fx_objects = manager.repository.receive()
        self.assertEqual(len(fx_objects), 3)
        for fx_object in fx_objects:
            self.assertEqual(fx_object.fx_rate, 1.0)
            self.assertEqual(fx_object.value_date, timezone.now().date())
            self.assertIn(fx_object.ccy_code, TEST_CURRENCY_CODES)
