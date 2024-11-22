from django.urls import reverse
from baseclasses.dataclasses.view_classes import TabElement, ActionElement
from baseclasses.pages import MontrekPage
from mt_economic_common.credit_institution.repositories.credit_institution_repository import (
    CreditInstitutionRepository,
)


class CreditInstitutionAppPage(MontrekPage):
    page_title = "Credit Institutions"

    def get_tabs(self):
        overview_tab = TabElement(
            name="Overview",
            link=reverse("credit_institution"),
            html_id="tab_overview",
        )
        return (overview_tab,)


class CreditInstitutionPage(MontrekPage):
    repository = CreditInstitutionRepository({})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "pk" not in kwargs:
            raise ValueError("AccountPage needs pk specified in url!")
        self.obj = self.repository.receive().get(pk=kwargs["pk"])
        self.page_title = self.obj.credit_institution_name

    def get_tabs(self):
        view_tab = TabElement(
            name="Details",
            link=reverse("credit_institution_details", args=[self.obj.id]),
            html_id="tab_details",
        )
        return (view_tab,)
