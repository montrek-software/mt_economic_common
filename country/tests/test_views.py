import os
import json
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, Mock

from mt_economic_common.country.tests.factories.country_factories import (
    CountryOecdFxAnnualTSSatelliteFactory,
    CountryStaticSatelliteFactory,
    CountryHubFactory,
    CountryApiUploadRegistryStaticSatelliteFactory,
)
from mt_economic_common.country import views
from mt_economic_common.country.repositories.country_repository import (
    CountryApiUploadRegistryRepository,
)
from user.tests.factories.montrek_user_factories import MontrekUserFactory
from testing.test_cases import view_test_cases as vtc


class TestCountryOverview(vtc.MontrekListViewTestCase):
    viewname = "country"
    view_class = views.CountryOverview
    expected_no_of_rows = 5

    def build_factories(self):
        CountryStaticSatelliteFactory.create_batch(5)


class TestCountryCreateView(vtc.MontrekCreateViewTestCase):
    viewname = "country_create"
    view_class = views.CountryCreateView

    def creation_data(self) -> dict:
        return {
            "country_name": "Germany",
            "country_code": "DEU",
            "country_code_2": "DE",
        }


class TestCountryDetailsView(vtc.MontrekDetailViewTestCase):
    viewname = "country_details"
    view_class = views.CountryDetailsView

    def build_factories(self):
        self.country = CountryStaticSatelliteFactory()

    def url_kwargs(self) -> dict:
        return {"pk": self.country.hub_entity.id}


class TestCountryUpdateView(vtc.MontrekUpdateViewTestCase):
    viewname = "country_update"
    view_class = views.CountryUpdateView

    def build_factories(self):
        self.country = CountryStaticSatelliteFactory()

    def url_kwargs(self) -> dict:
        return {"pk": self.country.hub_entity.id}


class TestUploadCountriesRestCountries(TestCase):
    def setUp(self):
        self.user = MontrekUserFactory()
        self.client.force_login(self.user)

    @patch("api_upload.managers.request_manager.requests.get")
    def test_upload_countries_rest_countries_returns_correct_html(self, mock_get):
        mock_response = Mock()
        with open(
            os.path.join(
                os.path.dirname(__file__), "test_data/rest_countries_example.json"
            )
        ) as f:
            mock_response.json.return_value = json.loads(f.read())
        mock_get.return_value = mock_response
        url = reverse("upload_countries_rest_countries")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("country"))
        registry_query = CountryApiUploadRegistryRepository().std_queryset()
        self.assertEqual(registry_query.count(), 1)


class TestUploadOecdCountryData(TestCase):
    def setUp(self):
        self.user = MontrekUserFactory()
        self.client.force_login(self.user)

    @patch("api_upload.managers.request_manager.requests.get")
    def test_upload_countries_rest_countries_returns_correct_html(self, mock_get):
        mock_response = Mock()
        with open(
            os.path.join(os.path.dirname(__file__), "test_data/fx_annual_example.json")
        ) as f:
            mock_response.json.return_value = json.loads(f.read())
        mock_get.return_value = mock_response
        url = reverse("upload_oecd_country_data")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("country"))
        registry_query = CountryApiUploadRegistryRepository().std_queryset()
        self.assertEqual(registry_query.count(), 1)


class TestCountryMapView(vtc.MontrekViewTestCase):
    viewname = "country_map"
    view_class = views.CountryMapView

    def build_factories(self):
        self.country_satellite = CountryStaticSatelliteFactory(
            country_google_maps_url="https://goo.gl/maps/g7QxxSFsWyTPKuzd7"
        )

    def url_kwargs(self) -> dict:
        return {"pk": self.country_satellite.hub_entity.id}


class TestCountryOecdDataView(vtc.MontrekListViewTestCase):
    viewname = "country_oecd_data"
    view_class = views.CountryOecdDataView
    expected_no_of_rows = 5

    def build_factories(self):
        self.country = CountryHubFactory()
        for _ in range(5):
            CountryOecdFxAnnualTSSatelliteFactory(hub_entity=self.country)
        country_2 = CountryHubFactory()
        for _ in range(5):
            CountryOecdFxAnnualTSSatelliteFactory(hub_entity=country_2)

    def url_kwargs(self) -> dict:
        return {"pk": self.country.id}


class TestCountryApiRegistryListView(vtc.MontrekListViewTestCase):
    viewname = "country_api_registry_list"
    view_class = views.CountryApiUploadRegistryListView
    expected_no_of_rows = 5

    def build_factories(self):
        CountryApiUploadRegistryStaticSatelliteFactory.create_batch(5)
