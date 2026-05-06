from django.test import TestCase
from user.tests.factories.montrek_user_factories import MontrekUserFactory

from mt_economic_common.country.managers.country_oecd_manager import (
    CountryOecdAnnualFxUploadManager,
    CountryOecdInflationUploadManager,
)
from mt_economic_common.country.managers.country_upload_processors import (
    OecdAnnualFxUploadProcessor,
    OecdInflationUploadProcessor,
)
from mt_economic_common.country.repositories.country_oecd_repository import (
    CountryOecdInflationRepository,
    CountryOecdRepository,
    CountryOecdTableRepository,
)
from mt_economic_common.country.tests.factories.country_factories import (
    CountryStaticSatelliteFactory,
)
from mt_economic_common.country.tests.mocks import MockOecdSdmxRequestManager
from mt_economic_common.country.tests.test_data.country_oecd_test_data import (
    TEST_OECD_COUNTRY_DATA,
)


class MockRequestManager(MockOecdSdmxRequestManager):
    def get_response(self, endpoint: str) -> dict | list:
        self.status_code = 200
        return TEST_OECD_COUNTRY_DATA


class MockOecdAnnualFxUploadProcessor(OecdAnnualFxUploadProcessor):
    request_manager_class = MockRequestManager


class MockCountryOecdAnnualFxUploadManager(CountryOecdAnnualFxUploadManager):
    processor_class = MockOecdAnnualFxUploadProcessor


class MockOecdInflationUploadProcessor(OecdInflationUploadProcessor):
    request_manager_class = MockRequestManager


class MockCountryOecdInflationUploadManager(CountryOecdInflationUploadManager):
    processor_class = MockOecdInflationUploadProcessor


class TestOecdCountryManager(TestCase):
    def setUp(self):
        self.user = MontrekUserFactory()
        self.country_factories = [
            CountryStaticSatelliteFactory(country_name="Austria", country_code="AUS"),
            CountryStaticSatelliteFactory(country_name="Australia", country_code="AUT"),
            CountryStaticSatelliteFactory(country_name="Belgium", country_code="BEL"),
            CountryStaticSatelliteFactory(country_name="Germany", country_code="DEU"),
        ]

    def test_get_oecd_annual_fx_average(self):
        # Arrange
        country_manager = MockCountryOecdAnnualFxUploadManager(
            session_data={"user_id": self.user.id}
        )
        # Act
        country_manager.process_import_data()
        # Assert
        registry_query = country_manager.registry_repository.receive()
        self.assertEqual(registry_query.count(), 1)
        test_query = CountryOecdRepository().receive()
        self.assertEqual(test_query.count(), 4)
        test_query = test_query.filter(annual_fx_average__isnull=False)
        check = [test_query[i].annual_fx_average for i in range(3)]
        check.sort()
        self.assertEqual(
            check,
            [16.355853, 446.000041, 585.911013],
        )
        for country in self.country_factories[1:]:
            country_oecd_repository = CountryOecdTableRepository(
                {"pk": country.hub_entity.get_hub_value_date().id}
            )
            test_query = country_oecd_repository.receive()
            self.assertTrue(test_query.count() > 0)
            test_object = test_query.first()
            self.assertEqual(test_object.value_date.month, 12)
            self.assertEqual(test_object.value_date.day, 31)

    def test_get_oecd_inflation_average(self):
        country_manager = MockCountryOecdInflationUploadManager(
            session_data={"user_id": self.user.id}
        )
        # Act
        country_manager.process_import_data()
        # Assert
        registry_query = country_manager.registry_repository.receive()
        self.assertEqual(registry_query.count(), 1)
        test_query = CountryOecdInflationRepository().receive()
        self.assertEqual(test_query.count(), 4)
        test_query = test_query.filter(inflation__isnull=False)
        check = [test_query[i].inflation for i in range(3)]
        check.sort()
        self.assertEqual(
            check,
            [16.355853, 446.000041, 585.911013],
        )
