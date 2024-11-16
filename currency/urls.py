from django.urls import path
from mt_economic_common.currency import views

urlpatterns = [
    path("", views.CurrencyOverview.as_view(), name="currency"),
    path("create", views.CurrencyCreateView.as_view(), name="currency_create"),
    path(
        "<int:pk>/details", views.CurrencyDetailView.as_view(), name="currency_details"
    ),
    path(
        "upload_yahoo_fx_rates",
        views.upload_yahoo_fx_rates,
        name="upload_yahoo_fx_rates",
    ),
]
