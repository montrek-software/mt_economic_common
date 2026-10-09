import json
import os
from unittest.mock import Mock, patch

from django.test import TestCase

from mt_economic_common.country.managers.country_request_manager import (
    RestCountriesRequestManager,
)
from mt_economic_common.country.tests.factories.country_api_credentials_sat_factories import (
    CountryApiCredentialsSatelliteFactory,
)


def build_response(objects: list, offset: int, more: bool) -> Mock:
    response = Mock()
    response.ok = True
    response.status_code = 200
    response.json.return_value = {
        "data": {
            "objects": objects,
            "meta": {
                "total": 2,
                "count": len(objects),
                "limit": 1,
                "offset": offset,
                "more": more,
            },
        }
    }
    return response


class TestRestCountriesRequestManager(TestCase):
    def setUp(self):
        CountryApiCredentialsSatelliteFactory(api_type="RestCountries", token="abc")
        with open(
            os.path.join(
                os.path.dirname(__file__), "../test_data/rest_countries_example.json"
            )
        ) as f:
            self.countries = json.loads(f.read())

    @patch("requesting.managers.request_manager.requests.get")
    def test_get_countries_as_json(self, mock_get):
        mock_get.side_effect = [
            build_response(self.countries[:1], 0, True),
            build_response(self.countries[1:], 1, False),
        ]
        rest_countries_request_manager = RestCountriesRequestManager({})
        rest_countries_request_manager.page_size = 1
        self.assertEqual(
            rest_countries_request_manager.base_url,
            "https://api.restcountries.com/countries/v5",
        )

        countries = rest_countries_request_manager.get_response("")

        self.assertEqual(countries, self.countries)
        self.assertEqual(rest_countries_request_manager.status_code, 200)
        self.assertEqual(mock_get.call_count, 2)
        first_call, second_call = mock_get.call_args_list
        self.assertEqual(
            first_call.args[0], "https://api.restcountries.com/countries/v5"
        )
        self.assertEqual(first_call.args[1]["offset"], 0)
        self.assertEqual(second_call.args[1]["offset"], 1)
        self.assertEqual(first_call.args[1]["limit"], 1)
        self.assertIn("codes.alpha_3", first_call.args[1]["response_fields"])
        self.assertEqual(first_call.kwargs["headers"]["Authorization"], "Bearer abc")

    @patch("requesting.managers.request_manager.requests.get")
    def test_get_countries__unexpected_format(self, mock_get):
        response = Mock()
        response.ok = True
        response.status_code = 200
        response.json.return_value = [{"name": "legacy"}]
        mock_get.return_value = response
        rest_countries_request_manager = RestCountriesRequestManager({})

        countries = rest_countries_request_manager.get_response("")

        self.assertEqual(countries, [])
        self.assertEqual(rest_countries_request_manager.status_code, 0)

    @patch("requesting.managers.request_manager.requests.get")
    def test_get_countries__no_api_key(self, mock_get):
        rest_countries_request_manager = RestCountriesRequestManager({})
        rest_countries_request_manager.authenticator.credentials = {"token": None}

        countries = rest_countries_request_manager.get_response("")

        self.assertEqual(countries, [])
        self.assertEqual(rest_countries_request_manager.status_code, 0)
        self.assertEqual(
            rest_countries_request_manager.message,
            "No API key for REST Countries configured",
        )
        mock_get.assert_not_called()
