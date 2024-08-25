from django.test import TestCase
from mt_economic_common.country.managers.country_report_manager import (
    CountryReportManager,
)
from mt_economic_common.country.tests.factories.country_factories import (
    CountryStaticSatelliteFactory,
)


class TestCountryReportManager(TestCase):
    def setUp(self) -> None:
        self.country = CountryStaticSatelliteFactory(country_name="Italy")

    def test_document_title(self):
        # Given
        session_data = {"pk": self.country.hub_entity.id}
        country_report_manager = CountryReportManager(session_data)
        # When
        result = country_report_manager.document_title
        # Then
        self.assertEqual(result, "Country Report: Italy")
