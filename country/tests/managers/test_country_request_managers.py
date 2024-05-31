import os
import json
from unittest.mock import patch, Mock
from django.test import TestCase
from mt_economic_common.country.managers.country_request_manager import (
    RestCountriesRequestManager,
)


class TestRestCountriesRequestManager(TestCase):
    @patch("api_upload.managers.request_manager.requests.get")
    def test_get_countries_as_json(self, mock_get):
        # Mock API
        mock_response = Mock()
        with open(
            os.path.join(
                os.path.dirname(__file__), "../test_data/rest_countries_example.json"
            )
        ) as f:
            mock_response.json.return_value = json.loads(f.read())
        mock_get.return_value = mock_response
        # Arrange
        rest_countries_request_manager = RestCountriesRequestManager()
        self.assertEqual(
            rest_countries_request_manager.base_url, "https://restcountries.com/v3.1/"
        )
        # Act
        countries = rest_countries_request_manager.get_json("all")
        # Assert
        self.assertIsNotNone(countries)
        self.assertGreater(len(countries), 0)
