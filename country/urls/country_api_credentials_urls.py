from django.urls import path
from baseclasses.views import MontrekNavigationRedirectView
from mt_economic_common.country.views.country_api_credentials_views import (
    CountryApiCredentialsListView,
)
from mt_economic_common.country.views.country_api_credentials_views import (
    CountryApiCredentialsCreateView,
)
from mt_economic_common.country.views.country_api_credentials_views import (
    CountryApiCredentialsUpdateView,
)
from mt_economic_common.country.views.country_api_credentials_views import (
    CountryApiCredentialsDeleteView,
)
from mt_economic_common.country.views.country_api_credentials_views import (
    CountryApiCredentialsDetailView,
)
from mt_economic_common.country.views.country_api_credentials_views import (
    CountryApiCredentialsHistoryView,
)

urlpatterns = [
    path(
        "country_api_credentials",
        MontrekNavigationRedirectView.as_view(
            access_module=__name__,
            pattern_name="country_api_credentials_list",
        ),
        name="country_api_credentials",
    ),
    path(
        "country_api_credentials/list",
        CountryApiCredentialsListView.as_view(),
        name="country_api_credentials_list",
    ),
    path(
        "country_api_credentials/create",
        CountryApiCredentialsCreateView.as_view(),
        name="country_api_credentials_create",
    ),
    path(
        "country_api_credentials/<int:pk>/delete",
        CountryApiCredentialsDeleteView.as_view(),
        name="country_api_credentials_delete",
    ),
    path(
        "country_api_credentials/<int:pk>/update",
        CountryApiCredentialsUpdateView.as_view(),
        name="country_api_credentials_update",
    ),
    path(
        "country_api_credentials/<int:pk>/details",
        CountryApiCredentialsDetailView.as_view(),
        name="country_api_credentials_details",
    ),
    path(
        "country_api_credentials/<int:pk>/history",
        CountryApiCredentialsHistoryView.as_view(),
        name="country_api_credentials_history",
    ),
]
