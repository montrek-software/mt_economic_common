from django.db.models import Q
from django.test import TestCase
from django.utils import timezone
from testing.decorators.add_logged_in_user import add_logged_in_user

from mt_economic_common.currency.models import CurrencyTimeSeriesSatellite
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)
from mt_economic_common.currency.tests.factories.currency_factories import (
    CurrencyHubFactory,
    CurrencyTimeSeriesSatelliteFactory,
)


class TestCurrencyRepositories(TestCase):
    @add_logged_in_user
    def setUp(self):
        self.session_data = {"user_id": self.user.id}

    def test_add_fx_rate_now(self):
        currency_hub = CurrencyHubFactory()
        currency_repo = CurrencyRepository(session_data=self.session_data)
        fx_rate = 1.23
        currency_repo.create_by_dict(
            {
                "hub_entity_id": currency_hub.id,
                "fx_rate": fx_rate,
                "value_date": timezone.now().date(),
            }
        )
        fx_object = currency_repo.receive().get()
        self.assertEqual(float(fx_object.fx_rate), fx_rate)
        self.assertEqual(fx_object.hub, currency_hub)
        self.assertEqual(fx_object.value_date, timezone.now().date())
