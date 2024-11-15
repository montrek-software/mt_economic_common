from mt_economic_common.currency.tests.factories.currency_factories import (
    CurrencyStaticSatelliteFactory,
)
from mt_economic_common.currency import views
from testing.test_cases import view_test_cases as vtc


class TestCurrencyCreate(vtc.MontrekCreateViewTestCase):
    viewname = "currency_create"
    view_class = views.CurrencyCreateView

    def creation_data(self) -> dict:
        return {
            "ccy_name": "test_currency",
            "ccy_code": "USD",
        }


class TestCurrencyDetails(vtc.MontrekDetailViewTestCase):
    viewname = "currency_details"
    view_class = views.CurrencyDetailView

    def build_factories(self):
        self.ccy = CurrencyStaticSatelliteFactory()

    def url_kwargs(self) -> dict:
        return {"pk": self.ccy.get_hub_value_date().id}


class TestCurrencyOverview(vtc.MontrekListViewTestCase):
    viewname = "currency"
    view_class = views.CurrencyOverview
    expected_no_of_rows = 5

    def build_factories(self):
        CurrencyStaticSatelliteFactory.create_batch(5)
