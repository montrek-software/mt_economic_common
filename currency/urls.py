from django.urls import path
from mt_economic_common.currency import views

urlpatterns = [
    path("", views.CurrencyOverview.as_view(), name="currency"),
    path("create", views.CurrencyCreateView.as_view(), name="currency_create"),
    path(
        "<int:pk>/details", views.CurrencyDetailView.as_view(), name="currency_details"
    ),
    path("fx_rate_import", views.FxRateImportView.as_view(), name="fx_rate_import"),
    path(
        "fx_rate_import_registry",
        views.FxRateImportRegistryView.as_view(),
        name="fx_rate_import_registry",
    ),
]
