from django.test import TestCase
import pandas as pd
from mt_economic_common.country.managers.country_upload_processors import (
    RestCountriesUploadProcessor,
)
from user.tests.factories.montrek_user_factories import MontrekUserFactory
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)


class TestRestCountryUploadProcessor(TestCase):
    def setUp(self):
        self.user = MontrekUserFactory()

    def test_process__raise_error_when_ccy_upload_fails(self):
        mailicious_json = [
            {
                "currencies": {
                    "ABC": {"namex": "First name", "symbol": "AB"},
                }
            },
            {
                "currencies": {
                    "ABC": {"name": "Second name", "symbol": "AB"},
                }
            },
        ]
        processor = RestCountriesUploadProcessor( {"user_id": self.user.id}, mailicious_json)
        processor.process()
        self.assertTrue(
            processor.message.startswith(
                "Error raised during object creation:",
            )
        )

    def test_create_currencies__return_list_of_currency_objects(self):
        processor = RestCountriesUploadProcessor({"user_id": self.user.id}, None)
        currencies = pd.Series(
            [
                {"ABC": {"name": "First name", "symbol": "AB"}},
                {"DEF": {"name": "Second name", "symbol": "DE"}},
                {"ABC": {"name": "Third name", "symbol": "AB"}},
            ]
        )
        result_sr = processor.create_currencies(currencies)
        self.assertEqual(result_sr.iloc[0], result_sr.iloc[2])
        currencies = CurrencyRepository().receive().all()
        self.assertEqual(len(currencies), 2)
        self.assertEqual(currencies[0].ccy_name, "First name")
