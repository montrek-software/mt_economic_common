import os
import json
from django.test import TestCase
from unittest.mock import patch, Mock
from mt_economic_common.country.repositories.country_oecd_repository import (
    CountryOecdRepository,
    CountryOecdTableRepository,
)
from user.tests.factories.montrek_user_factories import MontrekUserFactory
from mt_economic_common.country.tests.factories.country_factories import (
    CountryStaticSatelliteFactory,
)

from mt_economic_common.country.managers.country_oecd_manager import (
    CountryOecdAnnualFxUploadManager,
)


class TestOecdCountryManager(TestCase):
    def setUp(self):
        self.user = MontrekUserFactory()
        self.country_factories = [
            CountryStaticSatelliteFactory(country_name="Austria", country_code="AUS"),
            CountryStaticSatelliteFactory(country_name="Australia", country_code="AUT"),
            CountryStaticSatelliteFactory(country_name="Belgium", country_code="BEL"),
            CountryStaticSatelliteFactory(country_name="Germany", country_code="DEU"),
        ]

    @patch("api_upload.managers.request_manager.requests.get")
    def test_get_oecd_annual_fx_average(self, mock_get):
        mock_response = Mock()
        with open(
            os.path.join(
                os.path.dirname(__file__), "../test_data/fx_annual_example.json"
            )
        ) as f:
            mock_response.json.return_value = json.loads(f.read())
        mock_get.return_value = mock_response
        # Arrange
        country_manager = CountryOecdAnnualFxUploadManager(
            session_data={"user_id": self.user.id}
        )
        # Act
        country_manager.upload_and_process()
        # Assert
        registry_query = country_manager.repository.std_queryset()
        self.assertEqual(registry_query.count(), 1)
        test_query = CountryOecdRepository().std_queryset()
        self.assertEqual(test_query.count(), 4)
        self.assertEqual(
            [test_query[i].annual_fx_average for i in range(4)],
            [76.78634, 62.46608, 81.18251, None],
        )
        for country in self.country_factories[:-1]:
            country_oecd_repository = CountryOecdTableRepository(
                {"pk": country.hub_entity.id}
            )
            test_query = country_oecd_repository.std_queryset()
            self.assertEqual(test_query.count(), 4)
