from django.urls import reverse
from baseclasses.dataclasses.view_classes import ActionElement, ListActionElement
from baseclasses import views
from mt_economic_common.country.managers.country_api_credentials_managers import (
    CountryApiCredentialsTableManager,
)
from mt_economic_common.country.managers.country_api_credentials_managers import (
    CountryApiCredentialsDetailsManager,
)
from mt_economic_common.country.pages.country_api_credentials_pages import (
    CountryApiCredentialsPage,
)
from mt_economic_common.country.pages.country_api_credentials_pages import (
    CountryApiCredentialsDetailsPage,
)
from mt_economic_common.country.forms.country_api_credentials_forms import (
    CountryApiCredentialsCreateForm,
)


class CountryApiCredentialsCreateView(views.MontrekCreateView):
    manager_class = CountryApiCredentialsTableManager
    page_class = CountryApiCredentialsPage
    tab = "tab_country_api_credentials_list"
    form_class = CountryApiCredentialsCreateForm
    success_url = "country_api_credentials_list"
    title = "Country Api Credentials Create"


class CountryApiCredentialsUpdateView(views.MontrekUpdateView):
    manager_class = CountryApiCredentialsTableManager
    page_class = CountryApiCredentialsPage
    tab = "tab_country_api_credentials_list"
    form_class = CountryApiCredentialsCreateForm
    success_url = "country_api_credentials_list"
    title = "Country Api Credentials Update"


class CountryApiCredentialsDeleteView(views.MontrekDeleteView):
    manager_class = CountryApiCredentialsTableManager
    page_class = CountryApiCredentialsPage
    tab = "tab_country_api_credentials_list"
    success_url = "country_api_credentials_list"
    title = "Country Api Credentials Delete"


class CountryApiCredentialsListView(views.MontrekListView):
    manager_class = CountryApiCredentialsTableManager
    page_class = CountryApiCredentialsPage
    tab = "tab_country_api_credentials_list"
    title = "Country Api Credentials List"

    @property
    def actions(self) -> tuple:
        action_new = ActionElement(
            icon="plus",
            link=reverse("country_api_credentials_create"),
            action_id="id_create_country_api_credentials",
            hover_text="Create new Country Api Credentials",
        )
        return (action_new,)


class CountryApiCredentialsDetailView(views.MontrekDetailView):
    manager_class = CountryApiCredentialsDetailsManager
    page_class = CountryApiCredentialsDetailsPage
    tab = "tab_country_api_credentials_details"
    title = "Country Api Credentials Details"

    @property
    def actions(self) -> tuple:
        action_back = ListActionElement("country_api_credentials_list")
        return (action_back,)


class CountryApiCredentialsHistoryView(views.MontrekHistoryListView):
    manager_class = CountryApiCredentialsTableManager
    page_class = CountryApiCredentialsDetailsPage
    tab = "tab_country_api_credentials_history"
    title = "Country Api Credentials History"

    @property
    def actions(self) -> tuple:
        action_back = ListActionElement("country_api_credentials_list")
        return (action_back,)
