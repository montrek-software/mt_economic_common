import datetime
from decimal import Decimal

from django.urls import reverse

from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)
from mt_economic_common.currency.repositories.fx_rate_import_registry_repository import (
    FxRateImportRegistryRepository,
)
from mt_economic_common.currency.tests.factories.currency_factories import (
    CurrencyHubValueDateFactory,
    CurrencyStaticSatelliteFactory,
    CurrencyTimeSeriesSatelliteFactory,
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


class TestCurrencyReportView(vtc.MontrekReportViewTestCase):
    viewname = "currency_report"
    view_class = views.CurrencyReportView
    expected_number_of_report_elements = 4

    def build_factories(self):
        static = CurrencyStaticSatelliteFactory(ccy_name="US Dollar", ccy_code="USD")
        other_currency = CurrencyStaticSatelliteFactory(ccy_code="GBP")
        for hub, value_date, fx_rate in (
            (static.hub_entity, "2026-10-01", 0.89),
            (static.hub_entity, "2026-10-02", 0.8908686),
            (other_currency.hub_entity, "2026-10-02", 1.17),
        ):
            CurrencyTimeSeriesSatelliteFactory(
                hub_value_date=CurrencyHubValueDateFactory(
                    hub=hub, value_date=value_date
                ),
                fx_rate=fx_rate,
            )
        self.currency = CurrencyRepository({}).receive().get(ccy_code="USD")

    def url_kwargs(self) -> dict:
        return {"pk": self.currency.pk}

    def test_fx_rate_history(self):
        report_manager = self.view.manager
        rows = list(report_manager.history_manager.get_full_table())
        self.assertEqual(
            [(str(row.value_date), row.fx_rate) for row in rows],
            [
                ("2026-10-02", Decimal("0.8908686000")),
                ("2026-10-01", Decimal("0.8900000000")),
            ],
        )
        self.assertEqual(report_manager.document_title, "FX Rates: US Dollar (USD)")

    def test_fx_rate_plot(self):
        plot = self.view.manager._get_fx_rate_plot()
        line = plot.figure.data[0]
        self.assertEqual([str(x) for x in line.x], ["2026-10-01", "2026-10-02"])
        self.assertEqual(list(line.y), [0.89, 0.8908686])
