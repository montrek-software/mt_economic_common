from django.test import TestCase
from mt_economic_common.country.managers.country_report_manager import (
    CountryReportManager,
)
from mt_economic_common.country.tests.factories.country_factories import (
    CountryStaticSatelliteFactory,
)


class TestCountryReportManager(TestCase):
    def setUp(self) -> None:
        country = CountryStaticSatelliteFactory(country_name="Italy")
        session_data = {"pk": country.hub_entity.id}
        self.country_report_manager = CountryReportManager(session_data)

    def test_document_title(self):
        # Given
        # When
        result = self.country_report_manager.document_title
        # Then
        self.assertEqual(result, "Country Report: Italy")

    def test_get_wikipedia_section(self):
        wiki_test = self.country_report_manager.get_wikipedia_section()
        self.assertIn(
            "Italy, officially the Italian Republic, is a country in Southern and Western Europe. ",
            wiki_test,
        )
