from django.urls import reverse
from baseclasses.dataclasses.view_classes import ActionElement
from baseclasses.views import MontrekListView, MontrekDetailView, MontrekCreateView
from baseclasses.dataclasses.table_elements import (
    StringTableElement,
    LinkTableElement,
    LinkTextTableElement,
)
from mt_economic_common.credit_institution.managers.credit_institution_manager import (
    CreditInstitutionManager,
)
from mt_economic_common.credit_institution.pages import (
    CreditInstitutionAppPage,
    CreditInstitutionPage,
)
from mt_economic_common.credit_institution.repositories.credit_institution_repository import (
    CreditInstitutionRepository,
)
from mt_economic_common.credit_institution.forms import CreditInstitutionCreateForm

# Create your views here.


class CreditInstitutionOverview(MontrekListView):
    page_class = CreditInstitutionAppPage
    tab = "tab_overview"
    title = "Overview Table"
    manager_class = CreditInstitutionManager

    @property
    def elements(self) -> dict:
        return (
            StringTableElement(name="Name", attr="credit_institution_name"),
            LinkTableElement(
                name="Link",
                url="credit_institution_details",
                kwargs={"pk": "id"},
                icon="chevron-right",
                hover_text="Goto Credit Institution",
            ),
            StringTableElement(name="BIC", attr="credit_institution_bic"),
            StringTableElement(name="Upload Method", attr="account_upload_method"),
            LinkTextTableElement(
                name="Country",
                url="country_details",
                kwargs={"pk": "country_id"},
                text="country_name",
                hover_text="Goto Country",
            ),
        )

    @property
    def actions(self) -> tuple:
        action_create = ActionElement(
            icon="plus",
            link=reverse("credit_institution_create"),
            action_id="create_credit_institution",
            hover_text="Create Credit Institution",
        )
        return (action_create,)


class CreditInstitutionCreate(MontrekCreateView):
    page_class = CreditInstitutionAppPage
    manager_class = CreditInstitutionManager
    success_url = "credit_institution"
    form_class = CreditInstitutionCreateForm


class CreditIntitutionDetailView(MontrekDetailView):
    page_class = CreditInstitutionPage
    tab = "tab_details"
    manager_class = CreditInstitutionManager
    title = "Details"

    @property
    def elements(self) -> tuple:
        return (
            StringTableElement(name="Name", attr="credit_institution_name"),
            StringTableElement(name="BIC", attr="credit_institution_bic"),
            StringTableElement(name="Upload Method", attr="account_upload_method"),
        )

    @property
    def actions(self) -> tuple:
        action_back = ActionElement(
            icon="arrow-left",
            link=reverse("credit_institution"),
            action_id="back_to_overview",
            hover_text="Back to Overview",
        )
        return (action_back,)
