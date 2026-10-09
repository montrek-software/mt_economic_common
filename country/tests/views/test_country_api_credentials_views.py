from mt_economic_common.country.dataclasses.api_types import CountryApiTypeEnum
from testing.test_cases.view_test_cases import (
    TEST_USER_PASSWORD,
    MontrekCreateViewTestCase,
    MontrekUpdateViewTestCase,
    MontrekViewTestCase,
    MontrekListViewTestCase,
    MontrekDeleteViewTestCase,
)
from mt_economic_common.country.tests.factories.country_api_credentials_hub_factories import (
    CountryApiCredentialsHubValueDateFactory,
)
from mt_economic_common.country.tests.factories.country_api_credentials_sat_factories import (
    CountryApiCredentialsSatelliteFactory,
)
from mt_economic_common.country.views.country_api_credentials_views import (
    CountryApiCredentialsCreateView,
)
from mt_economic_common.country.views.country_api_credentials_views import (
    CountryApiCredentialsUpdateView,
)
from mt_economic_common.country.views.country_api_credentials_views import (
    CountryApiCredentialsListView,
)
from mt_economic_common.country.views.country_api_credentials_views import (
    CountryApiCredentialsDeleteView,
)
from mt_economic_common.country.views.country_api_credentials_views import (
    CountryApiCredentialsDetailView,
)
from mt_economic_common.country.views.country_api_credentials_views import (
    CountryApiCredentialsHistoryView,
)


class TestCountryApiCredentialsCreateView(MontrekCreateViewTestCase):
    viewname = "country_api_credentials_create"
    view_class = CountryApiCredentialsCreateView

    def creation_data(self):
        return {
            "api_type": CountryApiTypeEnum.REST_COUNTRIES.value.name,
            "token": TEST_USER_PASSWORD,
        }


class TestCountryApiCredentialsUpdateView(MontrekUpdateViewTestCase):
    viewname = "country_api_credentials_update"
    view_class = CountryApiCredentialsUpdateView

    def build_factories(self):
        self.sat_obj = CountryApiCredentialsSatelliteFactory()

    def url_kwargs(self) -> dict:
        return {"pk": self.sat_obj.get_hub_value_date().id}

    def update_data(self):
        return {
            "api_type": CountryApiTypeEnum.REST_COUNTRIES.value.name,
            "token": TEST_USER_PASSWORD,
        }


class TestCountryApiCredentialsListView(MontrekListViewTestCase):
    viewname = "country_api_credentials_list"
    view_class = CountryApiCredentialsListView
    expected_no_of_rows = 1

    def build_factories(self):
        self.sat_obj = CountryApiCredentialsSatelliteFactory()


class TestCountryApiCredentialsDeleteView(MontrekDeleteViewTestCase):
    viewname = "country_api_credentials_delete"
    view_class = CountryApiCredentialsDeleteView

    def build_factories(self):
        self.sat_obj = CountryApiCredentialsSatelliteFactory()

    def url_kwargs(self) -> dict:
        return {"pk": self.sat_obj.get_hub_value_date().id}


class TestCountryApiCredentialsDetailView(MontrekViewTestCase):
    viewname = "country_api_credentials_details"
    view_class = CountryApiCredentialsDetailView

    def build_factories(self):
        self.hub_vd = CountryApiCredentialsHubValueDateFactory(value_date=None)
        CountryApiCredentialsSatelliteFactory(hub_entity=self.hub_vd.hub)

    def url_kwargs(self) -> dict:
        return {"pk": self.hub_vd.hub.id}


class TestCountryApiCredentialsHistoryView(MontrekViewTestCase):
    viewname = "country_api_credentials_history"
    view_class = CountryApiCredentialsHistoryView

    def build_factories(self):
        self.hub_vd = CountryApiCredentialsHubValueDateFactory(value_date=None)
        CountryApiCredentialsSatelliteFactory(hub_entity=self.hub_vd.hub)

    def url_kwargs(self) -> dict:
        return {"pk": self.hub_vd.id}
