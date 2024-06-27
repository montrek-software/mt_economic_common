from django.test import TestCase
from mt_economic_common.country.managers.country_upload_processors import (
    RestCountriesUploadProcessor,
)
from user.tests.factories.montrek_user_factories import MontrekUserFactory


class TestRestCountryUploadProcessor(TestCase):
    def setUp(self):
        self.user = MontrekUserFactory()

    def test_process__raise_error_when_ccy_upload_fails(self):
        processor = RestCountriesUploadProcessor(None, {"user_id": self.user.id})
        mailicious_json = [
            {
                "currencies": {
                    "ABC": {"name": "First name", "symbol": "AB"},
                }
            },
            {
                "currencies": {
                    "ABC": {"name": "Second name", "symbol": "AB"},
                }
            },
        ]
        processor.process(mailicious_json)
        self.assertEqual(
            processor.message,
            "Error raised during object creation: ValueError: Duplicated entries found for CurrencyStaticSatellite with fields ['ccy_code']\n",
        )
