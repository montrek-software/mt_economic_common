from django.test import TestCase
from django.urls import reverse

from mt_economic_common.country.tests.factories.country_factories import (
    CountryStaticSatelliteFactory,
)
from mt_economic_common.country import views
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
            "country_code": "DE",
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

    def test_upload_countries_rest_countries_returns_correct_html(self):
        url = reverse("upload_countries_rest_countries")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("country"))


class TestCountryMapView(TestCase):
    def setUp(self):
        self.country_satellite = CountryStaticSatelliteFactory(
            country_google_maps_url="https://goo.gl/maps/g7QxxSFsWyTPKuzd7"
        )

    def test_country_map_returns_correct_html(self):
        url = reverse(
            "country_map", kwargs={"pk": self.country_satellite.hub_entity.id}
        )
        response = self.client.get(url)
        self.assertTemplateUsed(response, "country_map.html")
