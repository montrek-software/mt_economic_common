from django.urls import path
from mt_economic_common.credit_institution import views

urlpatterns = [
    path("", views.CreditInstitutionOverview.as_view(), name="credit_institution"),
    path(
        "create",
        views.CreditInstitutionCreate.as_view(),
        name="credit_institution_create",
    ),
    path(
        "<int:pk>/details",
        views.CreditIntitutionDetailView.as_view(),
        name="credit_institution_details",
    ),
]
