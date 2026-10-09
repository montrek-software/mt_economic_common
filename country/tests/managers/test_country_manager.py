from django.test import TestCase
from user.tests.factories.montrek_user_factories import MontrekUserFactory

from mt_economic_common.country.managers.country_manager import (
    RestCountriesUploadManager,
)
from mt_economic_common.country.managers.country_request_manager import (
    RestCountriesRequestManager,
)
from mt_economic_common.country.managers.country_upload_processors import (
    RestCountriesUploadProcessor,
)
from mt_economic_common.country.repositories.country_repository import CountryRepository
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)


def build_country(
    common: str,
    official: str,
    alpha_2: str,
    alpha_3: str,
    capital: str,
    currencies: list[dict],
) -> dict:
    return {
        "names": {"common": common, "official": official},
        "codes": {"alpha_2": alpha_2, "alpha_3": alpha_3},
        "coordinates": {"lat": 46.0, "lng": 2.0},
        "capitals": [
            {
                "name": capital,
                "coordinates": {"lat": 48.87, "lng": 2.33},
                "attributes": {"primary": True},
            }
        ],
        "postal_code": {"format": "#####", "regex": "^(\\d{5})$"},
        "links": {
            "google_maps": "https://goo.gl/maps/example",
            "open_street_maps": "https://www.openstreetmap.org/relation/1",
        },
        "flag": {"url_png": f"https://flags.restcountries.com/v5/w640/{alpha_2}.png"},
        "classification": {"un_member": True},
        "currencies": currencies,
        "continents": ["Europe"],
        "region": "Europe",
        "subregion": "Western Europe",
        "area": {"kilometers": 551695.0},
        "population": 67391582,
    }


class MockCountryRequestManager(RestCountriesRequestManager):
    base_url = "test_url"

    def get_response(self, endpoint: str):
        self.status_code = 200
        euro = {"code": "EUR", "name": "Euro", "symbol": "€"}
        return [
            build_country("France", "French Republic", "FR", "FRA", "Paris", [euro]),
            build_country(
                "Germany",
                "Federal Republic of Germany",
                "DE",
                "DEU",
                "Berlin",
                [euro, {"code": "DM", "name": "Deutsche Mark", "symbol": "DM"}],
            ),
            # Entities without ISO codes are skipped
            build_country("Abkhazia", "Republic of Abkhazia", "", "", "Sukhumi", []),
        ]


class MockRestCountriesUploadProcessor(RestCountriesUploadProcessor):
    request_manager_class = MockCountryRequestManager


class MockRestCountriesManager(RestCountriesUploadManager):
    processor_class = MockRestCountriesUploadProcessor


class TestCountryManager(TestCase):
    def setUp(self):
        self.user = MontrekUserFactory()

    def test_get_countries(self):
        # Arrange
        country_manager = MockRestCountriesManager(
            session_data={"user_id": self.user.id}
        )
        # Act
        country_manager.process_import_data()
        # Assert
        registry_query = country_manager.registry_repository.receive()
        self.assertEqual(registry_query.count(), 1)
        self.assertEqual(registry_query[0].import_status, "processed")

        test_query = CountryRepository().receive()
        self.assertEqual(test_query.count(), 2)
        self.assertEqual(test_query[0].country_name, "France")
        self.assertEqual(test_query[0].country_code, "FRA")
        self.assertEqual(test_query[0].country_code_2, "FR")
        self.assertEqual(test_query[1].country_name, "Germany")
        self.assertEqual(test_query[1].country_code, "DEU")
        self.assertEqual(test_query[1].country_code_2, "DE")
        self.assertEqual(
            test_query[1].country_official_name, "Federal Republic of Germany"
        )
        self.assertEqual(test_query[1].country_capital, "Berlin")
        self.assertEqual(test_query[1].country_continent, "Europe")
        self.assertEqual(test_query[1].country_region, "Europe")
        self.assertEqual(test_query[1].country_subregion, "Western Europe")
        self.assertTrue(test_query[1].country_un_member)
        self.assertEqual(test_query[1].country_lat, 46.0)
        self.assertEqual(test_query[1].country_long, 2.0)
        self.assertEqual(test_query[1].country_area, 551695.0)
        self.assertEqual(test_query[1].country_population, 67391582)
        self.assertEqual(test_query[1].country_postal_code_format, "#####")
        self.assertEqual(
            test_query[1].country_flag, "https://flags.restcountries.com/v5/w640/DE.png"
        )
        self.assertEqual(
            test_query[1].country_google_maps_url, "https://goo.gl/maps/example"
        )
        ccy_query = CurrencyRepository().receive().all()
        self.assertEqual(ccy_query.count(), 2)
        self.assertEqual(ccy_query[0].ccy_code, "EUR")
        self.assertEqual(ccy_query[0].ccy_name, "Euro")
        self.assertEqual(ccy_query[0].ccy_symbol, "€")
        self.assertEqual(ccy_query[1].ccy_code, "DM")
        self.assertEqual(ccy_query[1].ccy_name, "Deutsche Mark")
        self.assertEqual(ccy_query[1].ccy_symbol, "DM")
        self.assertEqual(test_query[0].ccy_code, '["EUR"]')
        self.assertEqual(test_query[1].ccy_code, '["EUR", "DM"]')
