from unittest import mock

from django.test import TestCase
from testing.decorators.mock_external_get import mock_external_get

from mt_economic_common.country.managers.country_report_manager import (
    CountryReportManager,
)
from mt_economic_common.country.tests.factories.country_factories import (
    CountryStaticSatelliteFactory,
)


class TestCountryReportManager(TestCase):
    def setUp(self) -> None:
        country = CountryStaticSatelliteFactory(country_name="Italy")
        session_data = {"pk": country.hub_entity.get_hub_value_date().id}
        self.country_report_manager = CountryReportManager(session_data)

    def test_document_title(self):
        # Given
        # When
        result = self.country_report_manager.document_title
        # Then
        self.assertEqual(result, "Country Report: Italy")

    @mock_external_get(
        response=mock.Mock(
            status_code=200,
            json=lambda: {
                "extract": "Italy, officially the Italian Republic, is a country in Southern and Western Europe. "
            },
        )
    )
    def test_get_wikipedia_section(self, mocked_get):
        wiki_test = self.country_report_manager.get_wikipedia_section()
        self.assertIn(
            "Italy, officially the Italian Republic, is a country in Southern and Western Europe. ",
            wiki_test,
        )
        mocked_get.assert_called_once()
