import datetime
from decimal import Decimal

from django.test import TestCase
from testing.decorators.add_logged_in_user import add_logged_in_user

from mt_economic_common.currency.constants import FX_SOURCE_KEY, FX_VALUE_DATE_KEY
from mt_economic_common.currency.managers.fx_rate_import_manager import (
    FxRateImportManager,
)
from mt_economic_common.currency.managers.fx_rate_import_processors import (
    DummyFxRateImportProcessor,
    FxRateImportProcessorABC,
)
from mt_economic_common.currency.managers.fx_rate_sources import FxRateSource
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)
from mt_economic_common.currency.tests.factories.currency_factories import (
    CurrencyStaticSatelliteFactory,
)

TEST_CURRENCY_CODES = ["EUR", "GBP", "USD"]
TEST_VALUE_DATE = datetime.date(2026, 10, 2)


class PartialFxRateImportProcessor(FxRateImportProcessorABC):
    def get_fx_rates(
        self, currency_codes: list[str], value_date: datetime.date
    ) -> dict[str, float]:
        return {"GBP": 1 / 20149.32}


class TestFxRateSource(TestCase):
    def test_to_list(self):
        self.assertIn(
            ("dummy", "Dummy (every FX rate set to 1)"), FxRateSource.to_list()
        )

    def test_from_label(self):
        self.assertEqual(FxRateSource.from_label("dummy"), FxRateSource.DUMMY)
        self.assertEqual(
            FxRateSource.DUMMY.value.processor_class, DummyFxRateImportProcessor
        )

    def test_from_unknown_label(self):
        with self.assertRaisesMessage(KeyError, "Unknown FX rate source 'yahoo'"):
            FxRateSource.from_label("yahoo")


class FxRateImportTestCase(TestCase):
    @add_logged_in_user
    def setUp(self):
        self.session_data = {"user_id": self.user.id}

    def create_currencies(self):
        for ccy_code in TEST_CURRENCY_CODES:
            CurrencyStaticSatelliteFactory(ccy_code=ccy_code)

    def get_registry(self, manager: FxRateImportManager):
        return manager.registry_repository.receive(apply_filter=False).get()


class TestFxRateImportManager(FxRateImportTestCase):
    def test_dummy_import_sets_all_rates_to_one(self):
        self.create_currencies()
        manager = FxRateImportManager(self.session_data)

        result = manager.import_fx_rates(FxRateSource.DUMMY, TEST_VALUE_DATE)

        self.assertTrue(result)
        fx_objects = CurrencyRepository(self.session_data).receive()
        self.assertEqual(
            sorted(fx_object.ccy_code for fx_object in fx_objects),
            TEST_CURRENCY_CODES,
        )
        for fx_object in fx_objects:
            self.assertEqual(fx_object.fx_rate, 1)
            self.assertEqual(fx_object.value_date, TEST_VALUE_DATE)
        registry = self.get_registry(manager)
        self.assertEqual(registry.import_status, "processed")
        self.assertEqual(registry.import_message, "Imported 3 FX rates for 2026-10-02")
        self.assertEqual(registry.fx_source, "dummy")
        self.assertEqual(registry.fx_value_date, TEST_VALUE_DATE)

    def test_import_fails_without_currencies(self):
        manager = FxRateImportManager(self.session_data)

        manager.import_fx_rates(FxRateSource.DUMMY, TEST_VALUE_DATE)

        registry = self.get_registry(manager)
        self.assertEqual(registry.import_status, "failed")
        self.assertEqual(
            registry.import_message, "No currencies found to import FX rates for"
        )
        self.assertEqual(registry.fx_source, "dummy")

    def test_import_fails_for_unknown_source(self):
        self.create_currencies()
        manager = FxRateImportManager(self.session_data)
        manager.set_pipeline_data(
            {FX_SOURCE_KEY: "yahoo", FX_VALUE_DATE_KEY: TEST_VALUE_DATE.isoformat()}
        )

        manager.trigger_pipeline()

        registry = self.get_registry(manager)
        self.assertEqual(registry.import_status, "failed")
        self.assertIn("Unknown FX rate source 'yahoo'", registry.import_message)


class TestFxRateImportProcessor(FxRateImportTestCase):
    def build_processor(self) -> PartialFxRateImportProcessor:
        processor = PartialFxRateImportProcessor(self.session_data, {})
        processor.set_pipeline_data({FX_VALUE_DATE_KEY: TEST_VALUE_DATE.isoformat()})
        return processor

    def test_missing_rates_are_reported(self):
        self.create_currencies()
        processor = self.build_processor()

        self.assertTrue(processor.pre_check())
        self.assertTrue(processor.process())
        self.assertTrue(processor.post_check())

        self.assertEqual(
            processor.message,
            "Imported 1 FX rates for 2026-10-02; no FX rate for EUR, USD",
        )

    def test_small_fx_rates_keep_precision(self):
        self.create_currencies()
        processor = self.build_processor()

        processor.pre_check()
        processor.process()

        gbp = CurrencyRepository(self.session_data).receive().get(ccy_code="GBP")
        self.assertEqual(gbp.fx_rate, Decimal("0.0000496295"))

    def test_base_class_requires_get_fx_rates(self):
        with self.assertRaisesMessage(
            NotImplementedError,
            "FxRateImportProcessorABC must implement get_fx_rates()",
        ):
            FxRateImportProcessorABC(self.session_data, {}).get_fx_rates(
                TEST_CURRENCY_CODES, TEST_VALUE_DATE
            )
