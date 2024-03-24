from django.test import TestCase
from mt_economic_common.country.managers.country_request_manager import (
    RestCountriesRequestManager,
)


class TestRestCountriesRequestManager(TestCase):
    def test_get_countries_as_json(self):
        # Arrange
        rest_countries_request_manager = RestCountriesRequestManager()
        self.assertEqual(
            rest_countries_request_manager.base_url, "https://restcountries.com/v3.1/"
        )
        # Act
        countries = rest_countries_request_manager.get_countries_as_json()
        # Assert
        self.assertIsNotNone(countries)
        self.assertGreater(len(countries), 0)
        self.assertEqual(rest_countries_request_manager.status_code, 200)
