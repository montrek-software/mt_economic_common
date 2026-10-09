import pandas as pd
from django.test import TestCase, override_settings
from user.tests.factories.montrek_user_factories import MontrekUserFactory

from mt_economic_common.country.managers.country_upload_processors import (
    RestCountriesUploadProcessor,
)
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)


class TestRestCountryUploadProcessor(TestCase):
    def setUp(self):
        self.user = MontrekUserFactory()

    @override_settings(IS_TEST_RUN=False)
    def test_process__raise_error_when_ccy_upload_fails(self):
        mailicious_json = [
            {"currencies": [{"codex": "ABC", "name": "First name", "symbol": "AB"}]},
            {"currencies": [{"code": "ABC", "name": "Second name", "symbol": "AB"}]},
        ]
        processor = RestCountriesUploadProcessor({"user_id": self.user.id}, None)
        processor.import_data = mailicious_json
        processor.process()
        self.assertTrue(
            processor.message.startswith(
                "Error raised during DataFrame transformation:",
            )
        )

    def test_create_currencies__return_list_of_currency_objects(self):
        processor = RestCountriesUploadProcessor({"user_id": self.user.id}, None)
        currencies = pd.Series(
            [
                [{"code": "ABC", "name": "First name", "symbol": "AB"}],
                [{"code": "DEF", "name": "Second name", "symbol": "DE"}],
                [{"code": "ABC", "name": "Third name", "symbol": "AB"}],
                [],
                None,
            ]
        )
        result_sr = processor.create_currencies(currencies)
        self.assertEqual(result_sr.iloc[0], result_sr.iloc[2])
        self.assertEqual(result_sr.iloc[3], [])
        self.assertEqual(result_sr.iloc[4], [])
        currencies = CurrencyRepository().receive().all()
        self.assertEqual(len(currencies), 2)
        self.assertEqual(currencies[0].ccy_name, "First name")
