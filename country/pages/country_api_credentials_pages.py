from django.urls import reverse
from baseclasses.dataclasses.view_classes import TabElement
from baseclasses.pages import MontrekDetailsPage, MontrekPage
from mt_economic_common.country.repositories.country_api_credentials_repositories import (
    CountryApiCredentialsRepository,
)

PAGE_TITLE = "Country Api Credentials"
LIST_TAB_NAME = "Country Api Credentials"
DETAILS_TAB_NAME = "Country Api Credentials"


class CountryApiCredentialsPage(MontrekPage):
    page_title = PAGE_TITLE

    def get_tabs(self):
        return (
            TabElement(
                name=LIST_TAB_NAME,
                link=reverse("country_api_credentials_list"),
                html_id="tab_country_api_credentials_list",
                active="active",
            ),
        )


class CountryApiCredentialsDetailsPage(MontrekDetailsPage):
    repository_class = CountryApiCredentialsRepository
    title_field = "hub_entity_id"

    def get_tabs(self):
        return (
            TabElement(
                name=DETAILS_TAB_NAME,
                link=reverse("country_api_credentials_details", args=[self.obj.id]),
                html_id="tab_country_api_credentials_details",
                active="active",
            ),
            TabElement(
                name="History",
                link=reverse("country_api_credentials_history", args=[self.obj.id]),
                html_id="tab_country_api_credentials_history",
            ),
        )
