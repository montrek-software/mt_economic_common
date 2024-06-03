from django.urls import reverse
from mt_economic_common.country.repositories.country_repository import CountryRepository
from baseclasses.dataclasses.view_classes import TabElement, ActionElement
from baseclasses.pages import MontrekPage


class CountryOverviewPage(MontrekPage):
    page_title = "Countries"

    def get_tabs(self):
        overview_tab = TabElement(
            name="Country List",
            link=reverse("country"),
            html_id="tab_country_list",
            active="active",
        )
        api_registry_tab = TabElement(
            name="API Registry",
            link=reverse("country_api_registry_list"),
            html_id="tab_country_api_registry",
        )
        return (overview_tab, api_registry_tab)


class CountryPage(MontrekPage):
    show_date_range_selector = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "pk" not in kwargs:
            raise ValueError("CountryPage needs pk specified in url!")
        self.obj = CountryRepository().std_queryset().get(pk=kwargs["pk"])
        self.page_title = self.obj.country_name

    def get_tabs(self):
        details_tab = TabElement(
            name="Details",
            link=reverse("country_details", args=[self.obj.id]),
            html_id="tab_details",
        )
        map_tab = TabElement(
            name="Map",
            link=reverse("country_map", args=[self.obj.id]),
            html_id="tab_map",
        )
        oecd_tab = TabElement(
            name="OECD Data",
            link=reverse("country_oecd_data", args=[self.obj.id]),
            html_id="tab_oecd_data",
        )
        return [details_tab, map_tab, oecd_tab]
