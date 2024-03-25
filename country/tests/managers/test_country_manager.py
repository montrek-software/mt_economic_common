from django.test import TestCase
from user.tests.factories.montrek_user_factories import MontrekUserFactory
from mt_economic_common.country.managers.country_manager import (
    RestCountriesManager,
)
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)


class MockCountryRequestManager:
    base_url = "test_url"

    def get_countries_as_json(self):
        return [
            {
                "name": {
                    "common": "France",
                    "official": "French Republic",
                    "nativeName": {
                        "fra": {"official": "République française", "common": "France"}
                    },
                },
                "tld": [".fr"],
                "cca2": "FR",
                "ccn3": "250",
                "cca3": "FRA",
                "cioc": "FRA",
                "independent": True,
                "status": "officially-assigned",
                "unMember": True,
                "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
                "idd": {"root": "+3", "suffixes": ["3"]},
                "capital": ["Paris"],
                "altSpellings": ["FR", "French Republic", "République française"],
                "region": "Europe",
                "subregion": "Western Europe",
                "languages": {"fra": "French"},
                "translations": {
                    "ara": {"official": "الجمهورية الفرنسية", "common": "فرنسا"},
                    "bre": {"official": "Republik Frañs", "common": "Frañs"},
                    "ces": {"official": "Francouzská republika", "common": "Francie"},
                    "cym": {"official": "French Republic", "common": "France"},
                    "deu": {
                        "official": "Französische Republik",
                        "common": "Frankreich",
                    },
                    "est": {"official": "Prantsuse Vabariik", "common": "Prantsusmaa"},
                    "fin": {"official": "Ranskan tasavalta", "common": "Ranska"},
                    "fra": {"official": "République française", "common": "France"},
                    "hrv": {"official": "Francuska Republika", "common": "Francuska"},
                    "hun": {
                        "official": "Francia Köztársaság",
                        "common": "Franciaország",
                    },
                    "ita": {"official": "Repubblica francese", "common": "Francia"},
                    "jpn": {"official": "フランス共和国", "common": "フランス"},
                    "kor": {"official": "프랑스 공화국", "common": "프랑스"},
                    "nld": {"official": "Franse Republiek", "common": "Frankrijk"},
                    "per": {"official": "جمهوری فرانسه", "common": "فرانسه"},
                    "pol": {"official": "Republika Francuska", "common": "Francja"},
                    "por": {"official": "República Francesa", "common": "França"},
                    "rus": {"official": "Французская Республика", "common": "Франция"},
                    "slk": {"official": "Francúzska republika", "common": "Francúzsko"},
                    "spa": {"official": "República francés", "common": "Francia"},
                    "srp": {"official": "Француска Република", "common": "Француска"},
                    "swe": {"official": "Republiken Frankrike", "common": "Frankrike"},
                    "tur": {"official": "Fransa Cumhuriyeti", "common": "Fransa"},
                    "urd": {"official": "جمہوریہ فرانس", "common": "فرانس"},
                    "zho": {"official": "法兰西共和国", "common": "法国"},
                },
                "latlng": [46.0, 2.0],
                "landlocked": False,
                "borders": ["AND", "BEL", "DEU", "ITA", "LUX", "MCO", "ESP", "CHE"],
                "area": 551695.0,
                "demonyms": {
                    "eng": {"f": "French", "m": "French"},
                    "fra": {"f": "Française", "m": "Français"},
                },
                "flag": "\uD83C\uDDEB\uD83C\uDDF7",
                "maps": {
                    "googleMaps": "https://goo.gl/maps/g7QxxSFsWyTPKuzd7",
                    "openStreetMaps": "https://www.openstreetmap.org/relation/1403916",
                },
                "population": 67391582,
                "gini": {"2018": 32.4},
                "fifa": "FRA",
                "car": {"signs": ["F"], "side": "right"},
                "timezones": [
                    "UTC-10:00",
                    "UTC-09:30",
                    "UTC-09:00",
                    "UTC-08:00",
                    "UTC-04:00",
                    "UTC-03:00",
                    "UTC+01:00",
                    "UTC+02:00",
                    "UTC+03:00",
                    "UTC+04:00",
                    "UTC+05:00",
                    "UTC+10:00",
                    "UTC+11:00",
                    "UTC+12:00",
                ],
                "continents": ["Europe"],
                "flags": {
                    "png": "https://flagcdn.com/w320/fr.png",
                    "svg": "https://flagcdn.com/fr.svg",
                    "alt": "The flag of France is composed of three equal vertical bands of blue, white and red.",
                },
                "coatOfArms": {
                    "png": "https://mainfacts.com/media/images/coats_of_arms/fr.png",
                    "svg": "https://mainfacts.com/media/images/coats_of_arms/fr.svg",
                },
                "startOfWeek": "monday",
                "capitalInfo": {"latlng": [48.87, 2.33]},
                "postalCode": {"format": "#####", "regex": "^(\\d{5})$"},
            },
            {
                "name": {
                    "common": "Germany",
                    "official": "Federal Republic of Germany",
                    "nativeName": {
                        "deu": {
                            "official": "Bundesrepublik Deutschland",
                            "common": "Deutschland",
                        }
                    },
                },
                "tld": [".de"],
                "cca2": "DE",
                "ccn3": "276",
                "cca3": "DEU",
                "cioc": "GER",
                "independent": True,
                "status": "officially-assigned",
                "unMember": True,
                "currencies": {
                    "EUR": {"name": "Euro", "symbol": "€"},
                    "DM": {"name": "Deutsche Mark", "symbol": "DM"},
                },
                "idd": {"root": "+4", "suffixes": ["9"]},
                "capital": ["Berlin"],
                "altSpellings": [
                    "DE",
                    "Federal Republic of Germany",
                    "Bundesrepublik Deutschland",
                ],
                "region": "Europe",
                "subregion": "Western Europe",
                "languages": {"deu": "German"},
                "translations": {
                    "ara": {
                        "official": "جمهورية ألمانيا الاتحادية",
                        "common": "ألمانيا",
                    },
                    "bre": {
                        "official": "Republik Kevreadel Alamagn",
                        "common": "Alamagn",
                    },
                    "ces": {
                        "official": "Spolková republika Německo",
                        "common": "Německo",
                    },
                    "cym": {
                        "official": "Federal Republic of Germany",
                        "common": "Germany",
                    },
                    "deu": {
                        "official": "Bundesrepublik Deutschland",
                        "common": "Deutschland",
                    },
                    "est": {"official": "Saksamaa Liitvabariik", "common": "Saksamaa"},
                    "fin": {"official": "Saksan liittotasavalta", "common": "Saksa"},
                    "fra": {
                        "official": "République fédérale d'Allemagne",
                        "common": "Allemagne",
                    },
                    "hrv": {
                        "official": "Njemačka Federativna Republika",
                        "common": "Njemačka",
                    },
                    "hun": {
                        "official": "Német Szövetségi Köztársaság",
                        "common": "Németország",
                    },
                    "ita": {
                        "official": "Repubblica federale di Germania",
                        "common": "Germania",
                    },
                    "jpn": {"official": "ドイツ連邦共和国", "common": "ドイツ"},
                    "kor": {"official": "독일 연방 공화국", "common": "독일"},
                    "nld": {
                        "official": "Bondsrepubliek Duitsland",
                        "common": "Duitsland",
                    },
                    "per": {"official": "جمهوری فدرال آلمان", "common": "آلمان"},
                    "pol": {
                        "official": "Republika Federalna Niemiec",
                        "common": "Niemcy",
                    },
                    "por": {
                        "official": "República Federal da Alemanha",
                        "common": "Alemanha",
                    },
                    "rus": {
                        "official": "Федеративная Республика Германия",
                        "common": "Германия",
                    },
                    "slk": {
                        "official": "Nemecká spolková republika",
                        "common": "Nemecko",
                    },
                    "spa": {
                        "official": "República Federal de Alemania",
                        "common": "Alemania",
                    },
                    "srp": {
                        "official": "Савезна Република Немачка",
                        "common": "Немачка",
                    },
                    "swe": {
                        "official": "Förbundsrepubliken Tyskland",
                        "common": "Tyskland",
                    },
                    "tur": {
                        "official": "Almanya Federal Cumhuriyeti",
                        "common": "Almanya",
                    },
                    "urd": {"official": "وفاقی جمہوریہ جرمنی", "common": "جرمنی"},
                    "zho": {"official": "德意志联邦共和国", "common": "德国"},
                },
                "latlng": [51.0, 9.0],
                "landlocked": False,
                "borders": [
                    "AUT",
                    "BEL",
                    "CZE",
                    "DNK",
                    "FRA",
                    "LUX",
                    "NLD",
                    "POL",
                    "CHE",
                ],
                "area": 357114.0,
                "demonyms": {
                    "eng": {"f": "German", "m": "German"},
                    "fra": {"f": "Allemande", "m": "Allemand"},
                },
                "flag": "\uD83C\uDDE9\uD83C\uDDEA",
                "maps": {
                    "googleMaps": "https://goo.gl/maps/mD9FBMq1nvXUBrkv6",
                    "openStreetMaps": "https://www.openstreetmap.org/relation/51477",
                },
                "population": 83240525,
                "gini": {"2016": 31.9},
                "fifa": "GER",
                "car": {"signs": ["DY"], "side": "right"},
                "timezones": ["UTC+01:00"],
                "continents": ["Europe"],
                "flags": {
                    "png": "https://flagcdn.com/w320/de.png",
                    "svg": "https://flagcdn.com/de.svg",
                    "alt": "The flag of Germany is composed of three equal horizontal bands of black, red and gold.",
                },
                "coatOfArms": {
                    "png": "https://mainfacts.com/media/images/coats_of_arms/de.png",
                    "svg": "https://mainfacts.com/media/images/coats_of_arms/de.svg",
                },
                "startOfWeek": "monday",
                "capitalInfo": {"latlng": [52.52, 13.4]},
                "postalCode": {"format": "#####", "regex": "^(\\d{5})$"},
            },
        ]


class MockRestCountriesManager(RestCountriesManager):
    request_manager = MockCountryRequestManager()


class TestCountryManager(TestCase):
    def setUp(self):
        self.user = MontrekUserFactory()

    def test_get_countries(self):
        # Arrange
        country_manager = MockRestCountriesManager(
            session_data={"user_id": self.user.id}
        )
        # Act
        country_manager.write_countries_to_db()
        # Assert
        test_query = country_manager.repository.std_queryset()
        self.assertEqual(test_query.count(), 2)
        self.assertEqual(test_query[0].country_name, "France")
        self.assertEqual(test_query[0].country_code, "FR")
        self.assertEqual(test_query[1].country_name, "Germany")
        self.assertEqual(test_query[1].country_code, "DE")
        ccy_query = CurrencyRepository().std_queryset().all()
        self.assertEqual(ccy_query.count(), 2)
        self.assertEqual(ccy_query[0].ccy_code, "EUR")
        self.assertEqual(ccy_query[0].ccy_name, "Euro")
        self.assertEqual(ccy_query[0].ccy_symbol, "€")
        self.assertEqual(ccy_query[1].ccy_code, "DM")
        self.assertEqual(ccy_query[1].ccy_name, "Deutsche Mark")
        self.assertEqual(ccy_query[1].ccy_symbol, "DM")
        self.assertEqual(test_query[0].country_ccy, ["EUR"])
        self.assertEqual(test_query[1].country_ccy, ["EUR", "DM"])
