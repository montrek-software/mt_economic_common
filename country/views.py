from django.contrib import messages
from django.urls import reverse
from django.views.generic.base import HttpResponseRedirect

from baseclasses.views import (
    MontrekCreateView,
    MontrekListView,
    MontrekDetailView,
    MontrekReportView,
    MontrekRestApiView,
    MontrekUpdateView,
    MontrekTemplateView,
)
from baseclasses.dataclasses.view_classes import ActionElement
from mt_economic_common.country.pages import CountryOverviewPage, CountryPage
from mt_economic_common.country.forms import CountryCreateForm
from mt_economic_common.country.managers.country_manager import (
    CountryManager,
    RestCountriesUploadManager,
    CountryTableManager,
    CountryDetailsManager,
    CountryApiUploadRegistryManager,
)
from mt_economic_common.country.managers.country_oecd_manager import (
    CountryOecdAnnualFxUploadManager,
    CountryOecdInflationUploadManager,
    CountryOecdTableManager,
    CountryOecdDataApiManager,
)
from mt_economic_common.country.managers.country_report_manager import (
    CountryReportManager,
)


class CountryCreateView(MontrekCreateView):
    page_class = CountryOverviewPage
    manager_class = CountryManager
    title = "Country"
    form_class = CountryCreateForm
    success_url = "country"


class CountryOverview(MontrekListView):
    page_class = CountryOverviewPage
    manager_class = CountryTableManager
    tab = "tab_country_list"
    title = "Country Overview"

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
        action_upload_oecd_data = ActionElement(
            icon="upload",
            link=reverse("upload_oecd_country_data"),
            action_id="id_upload_oecd_country_data",
            hover_text="Upload OECD data",
        )
        return (action_new_country, action_upload_countries, action_upload_oecd_data)


class CountryApiUploadRegistryListView(MontrekListView):
    page_class = CountryOverviewPage
    manager_class = CountryApiUploadRegistryManager
    title = "Country API Registry"
    tab = "tab_country_api_registry"


class CountryDetailsView(MontrekDetailView):
    page_class = CountryPage
    manager_class = CountryDetailsManager
    tab = "tab_details"
    title = "Country Details"

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
    manager_class = CountryManager
    title = "Country Update"
    form_class = CountryCreateForm
    success_url = "country"


def upload_countries_rest_countries(request):
    man = RestCountriesUploadManager(session_data={"user_id": request.user.id})
    man.upload_and_process()
    for m in man.messages:
        getattr(messages, m.message_type)(request, m.message)
    return HttpResponseRedirect(reverse("country"))


def upload_oecd_country_data(request):
    session_data = {"user_id": request.user.id}
    managers = (
        CountryOecdAnnualFxUploadManager(session_data=session_data),
        CountryOecdInflationUploadManager(session_data=session_data),
    )
    for man in managers:
        man.upload_and_process()
        for m in man.messages:
            getattr(messages, m.message_type)(request, m.message)
    return HttpResponseRedirect(reverse("country"))


class CountryMapView(MontrekTemplateView):
    page_class = CountryPage
    template_name = "country_map.html"
    manager_class = CountryManager
    title = "Map"
    tab = "tab_map"

    def get_template_context(self) -> dict:
        country = self.manager.repository.std_queryset().get(id=self.kwargs["pk"])
        long = country.country_long
        lat = country.country_lat
        long = long if long else 0
        lat = lat if lat else 90
        box_coords = [long - 5, lat + 5, long + 5, lat - 5]
        embedded_url = f"https://www.openstreetmap.org/export/embed.html?bbox={box_coords[0]}%2C{box_coords[3]}%2C{box_coords[2]}%2C{box_coords[1]}&layer=mapnik&marker={lat}%2C{long}"
        google_maps_url = country.country_google_maps_url
        google_maps_url = (
            google_maps_url if google_maps_url else "https://www.google.com/maps"
        )
        open_street_map_url = country.country_open_street_map_url
        open_street_map_url = (
            open_street_map_url
            if open_street_map_url
            else "https://www.openstreetmap.org"
        )
        return {
            "country_google_maps_url": google_maps_url,
            "country_open_street_map_url": open_street_map_url,
            "embedded_url": embedded_url,
        }

    @property
    def actions(self) -> tuple:
        action_back = ActionElement(
            icon="arrow-left",
            link=reverse("country"),
            action_id="back_to_overview",
            hover_text="Back to Overview",
        )
        return (action_back,)


class CountryOecdDataView(MontrekListView):
    page_class = CountryPage
    manager_class = CountryOecdTableManager
    tab = "tab_oecd_data"
    title = "OECD Data"

    @property
    def actions(self) -> tuple:
        action_back = ActionElement(
            icon="arrow-left",
            link=reverse("country"),
            action_id="back_to_overview",
            hover_text="Back to Overview",
        )
        return (action_back,)


class CountryReportView(MontrekReportView):
    page_class = CountryPage
    manager_class = CountryReportManager
    tab = "tab_report"

    @property
    def actions(self) -> tuple:
        action_back = ActionElement(
            icon="arrow-left",
            link=reverse("country"),
            action_id="back_to_overview",
            hover_text="Back to Overview",
        )
        return (action_back,)


class CountryOecdDataApiView(MontrekRestApiView):
    manager_class = CountryOecdDataApiManager
