from django.test import TestCase
from django.urls import reverse

from mt_economic_common.country.repositories.country_repository import CountryRepository
from mt_economic_common.country.tests.factories.country_factories import (
    CountryStaticSatelliteFactory,
)
from user.tests.factories.montrek_user_factories import MontrekUserFactory


class TestCountryOverview(TestCase):
    def test_country_overview_returns_correct_html(self):
        url = reverse("country")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "montrek_table.html")


class TestCountryCreateView(TestCase):
    def setUp(self):
        self.user = MontrekUserFactory()
        self.client.force_login(self.user)

    def test_country_create_returns_correct_html(self):
        url = reverse("country_create")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "montrek_create.html")

    def test_view_post_success(self):
        url = reverse("country_create")
        response = self.client.post(
            url,
            {
                "country_name": "Germany",
                "country_code": "DE",
            },
        )
        self.assertEqual(response.status_code, 302)
        country = CountryRepository().std_queryset().first()
        self.assertEqual(country.country_name, "Germany")
        self.assertEqual(country.country_code, "DE")


class TestCountryDetailsView(TestCase):
    def test_country_details_returns_correct_html(self):
        country = CountryStaticSatelliteFactory()
        url = reverse("country_details", kwargs={"pk": country.hub_entity.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "montrek_details.html")


class TestCountryUpdateView(TestCase):
    def test_country_update_returns_correct_html(self):
        country = CountryStaticSatelliteFactory()
        url = reverse("country_update", kwargs={"pk": country.hub_entity.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "montrek_create.html")


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
