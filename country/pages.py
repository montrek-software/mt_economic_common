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
        return (overview_tab,)


class CountryPage(MontrekPage):
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
        return [details_tab]
