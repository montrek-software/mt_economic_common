from django.urls import reverse

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
            table_elements.StringTableElement(
                name="Country Name",
                attr="country_name",
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
        return (action_new_country,)


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
                name="Country Code",
                attr="country_code",
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
