from logging import warn
from django.urls import reverse
from django.views.generic.base import HttpResponseRedirect

from baseclasses.views import (
    MontrekCreateView,
    MontrekListView,
    MontrekDetailView,
    MontrekUpdateView,
)
from baseclasses.dataclasses import table_elements
from baseclasses.dataclasses.view_classes import ActionElement
from mt_economic_common.country.pages import CountryOverviewPage, CountryPage
from mt_economic_common.country.repositories.country_repository import CountryRepository
from mt_economic_common.country.forms import CountryCreateForm
from mt_economic_common.country.managers.country_manager import RestCountriesManager


class CountryCreateView(MontrekCreateView):
    page_class = CountryOverviewPage
    repository = CountryRepository
    title = "Country"
    form_class = CountryCreateForm
    success_url = "country"


class CountryOverview(MontrekListView):
    page_class = CountryOverviewPage
    tab = "tab_country_list"
    title = "Country Overview"
    repository = CountryRepository

    @property
    def elements(self) -> tuple:
        return (
            table_elements.LinkTextTableElement(
                name="Country Name",
                url="country_details",
                kwargs={"pk": "id"},
                text="country_name",
                hover_text="View Country",
            ),
            table_elements.StringTableElement(
                name="Country Code",
                attr="country_code",
            ),
        )

    @property
    def actions(self) -> tuple:
        action_new_country = ActionElement(
            icon="plus",
            link=reverse("country_create"),
            action_id="id_create_country",
            hover_text="Create country",
        )
        action_upload_countries = ActionElement(
            icon="upload",
            link=reverse("upload_countries_rest_countries"),
            action_id="id_upload_countries",
            hover_text="Upload countries from RestCountries.com",
        )
        return (action_new_country, action_upload_countries)


class CountryDetailsView(MontrekDetailView):
    page_class = CountryPage
    repository = CountryRepository
    tab = "tab_details"
    title = "Country Details"

    @property
    def elements(self) -> tuple:
        return (
            table_elements.StringTableElement(
                name="Country Name",
                attr="country_name",
            ),
            table_elements.StringTableElement(
                name="Country Official Name",
                attr="country_official_name",
            ),
            table_elements.StringTableElement(
                name="Country Code",
                attr="country_code",
            ),
            table_elements.ImageTableElement(
                name="Flag",
                attr="country_flag",
            ),
            table_elements.FloatTableElement(
                name="Country Latitude",
                attr="country_lat",
            ),
            table_elements.FloatTableElement(
                name="Country Longitude",
                attr="country_long",
            ),
            table_elements.StringTableElement(
                name="Country Capital",
                attr="country_capital",
            ),
            table_elements.StringTableElement(
                name="Country Region",
                attr="country_region",
            ),
            table_elements.StringTableElement(
                name="Country Subregion",
                attr="country_subregion",
            ),
            table_elements.StringTableElement(
                name="Country Continent",
                attr="country_continent",
            ),
            table_elements.IntTableElement(
                name="Country Area",
                attr="country_area",
            ),
            table_elements.IntTableElement(
                name="Country Population",
                attr="country_population",
            ),
            table_elements.BooleanTableElement(
                name="UN Member",
                attr="country_un_member",
            ),
            table_elements.StringTableElement(
                name="Postal Code Format",
                attr="country_postal_code_format",
            ),
            table_elements.StringTableElement(
                name="Postal Code Regex",
                attr="country_postal_code_regex",
            ),
        )

    @property
    def actions(self) -> tuple:
        action_back = ActionElement(
            icon="arrow-left",
            link=reverse("country"),
            action_id="back_to_overview",
            hover_text="Back to Overview",
        )
        action_update_country = ActionElement(
            icon="pencil",
            link=reverse("country_update", kwargs={"pk": self.kwargs["pk"]}),
            action_id="id_update_country",
            hover_text="Update Country",
        )
        return (action_back, action_update_country)


class CountryUpdateView(MontrekUpdateView):
    page_class = CountryPage
    repository = CountryRepository
    title = "Country Update"
    form_class = CountryCreateForm
    success_url = "country"


def upload_countries_rest_countries(request):
    man = RestCountriesManager(session_data={"user_id": request.user.id})
    man.write_countries_to_db()
    return HttpResponseRedirect(reverse("country"))
