import datetime

from django.urls import reverse

from mt_economic_common.currency.repositories.fx_rate_import_registry_repository import (
    FxRateImportRegistryRepository,
)
from mt_economic_common.currency.tests.factories.currency_factories import (
    CurrencyStaticSatelliteFactory,
    FxRateImportRegistrySatelliteFactory,
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
        return {"pk": self.ccy.hub_entity.id}


class TestCurrencyOverview(vtc.MontrekListViewTestCase):
    viewname = "currency"
    view_class = views.CurrencyOverview
    expected_no_of_rows = 5

    def build_factories(self):
        CurrencyStaticSatelliteFactory.create_batch(5)


class TestFxRateImportView(vtc.MontrekViewTestCase):
    viewname = "fx_rate_import"
    view_class = views.FxRateImportView

    def test_form_is_shown(self):
        form = self.response.context["import_form"]
        self.assertEqual(list(form.fields), ["fx_source", "fx_value_date"])

    def test_post_triggers_import(self):
        CurrencyStaticSatelliteFactory(ccy_code="USD")

        response = self.client.post(
            self.url, {"fx_source": "dummy", "fx_value_date": "2026-10-02"}
        )

        self.assertRedirects(response, reverse("fx_rate_import_registry"))
        registry = FxRateImportRegistryRepository({}).receive(apply_filter=False).get()
        self.assertEqual(registry.import_status, "processed")
        self.assertEqual(registry.fx_source, "dummy")
        self.assertEqual(registry.fx_value_date, datetime.date(2026, 10, 2))

    def test_post_with_unknown_source_shows_form_errors(self):
        response = self.client.post(
            self.url, {"fx_source": "yahoo", "fx_value_date": "2026-10-02"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("fx_source", response.context["import_form"].errors)
        self.assertFalse(
            FxRateImportRegistryRepository({}).receive(apply_filter=False).exists()
        )


class TestFxRateImportRegistryView(vtc.MontrekListViewTestCase):
    viewname = "fx_rate_import_registry"
    view_class = views.FxRateImportRegistryView
    expected_no_of_rows = 2
    expected_columns = ["Source", "Value Date", "Import Status"]

    def build_factories(self):
        FxRateImportRegistrySatelliteFactory.create_batch(2)
