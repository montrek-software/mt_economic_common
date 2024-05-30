import os
import json
from django.test import TestCase
from unittest.mock import patch, Mock
from mt_economic_common.oecd_api.managers.oecd_request_manager import OecdRequestManager
from mt_economic_common.country.tests.factories.country_factories import (
    CountryStaticSatelliteFactory,
)
from mt_economic_common.currency.tests.factories.currency_factories import (
    CurrencyStaticSatelliteFactory,
)


class TestOecdRequestManager(TestCase):
    def setUp(self):
        for cnt, ccy in (
            ("AUS", "EUR"),
            ("AUT", "AUD"),
            ("BEL", "EUR"),
            ("CAN", "USD"),
        ):
            country_factory = CountryStaticSatelliteFactory(
                country_code=cnt, country_name=cnt
            )
            currency_factory = CurrencyStaticSatelliteFactory(
                ccy_code=ccy, ccy_name=ccy
            )
            country_factory.hub_entity.link_country_currency.add(
                currency_factory.hub_entity
            )

    def test_get_endpoint_url(self):
        manager = OecdRequestManager()
        endpoint = "test_endpoint"
        expected_url = (
            "https://sdmx.oecd.org/public/rest/data/test_endpoint&format=jsondata"
        )
        self.assertEqual(manager.get_endpoint_url(endpoint), expected_url)

    @patch("api_upload.managers.request_manager.requests.get")
    def test_get_fx_annual(self, mock_get):
        mock_response = Mock()
        with open(
            os.path.join(
                os.path.dirname(__file__), "../test_data/fx_annual_example.json"
            )
        ) as f:
            mock_response.json.return_value = json.loads(f.read())
        mock_get.return_value = mock_response
        manager = OecdRequestManager()
        result_df = manager.get_average_annual_fx_rates()
        self.assertEqual(result_df.shape, (16, 10))
        self.assertEqual(
            result_df.columns.tolist(),
            [
                "REF_AREA",
                "FREQ",
                "METHODOLOGY",
                "MEASURE",
                "UNIT_MEASURE",
                "EXPENDITURE",
                "ADJUSTMENT",
                "TRANSFORMATION",
                "TIME_PERIOD",
                "VALUE",
            ],
        )
        self.assertEqual(result_df["VALUE"].sum(), 1143.22449)
