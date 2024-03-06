from django.urls import reverse
from baseclasses.dataclasses.view_classes import ActionElement
from baseclasses.views import MontrekListView
from baseclasses.views import MontrekDetailView
from baseclasses.views import MontrekCreateView
from baseclasses.dataclasses.table_elements import (
    StringTableElement,
    LinkTableElement,
    FloatTableElement,
)
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)
from mt_economic_common.currency.pages import CurrencyAppPage
from mt_economic_common.currency.pages import CurrencyPage
from mt_economic_common.currency.forms import CurrencyCreateForm

# Create your views here.


class CurrencyOverview(MontrekListView):
    page_class = CurrencyAppPage
    tab = "tab_overview"
    title = "Overview Table"
    repository = CurrencyRepository

    @property
    def elements(self) -> dict:
        return (
            StringTableElement(name="Name", attr="ccy_name"),
            StringTableElement(name="Code", attr="ccy_code"),
            FloatTableElement(name="FX Rate", attr="fx_rate"),
            LinkTableElement(
                name="Link",
                url="currency_details",
                kwargs={"pk": "id"},
                icon="chevron-right",
                hover_text="Goto Currency",
            ),
        )

    @property
    def actions(self) -> tuple:
        action_new_currency = ActionElement(
            icon="plus",
            link=reverse("currency_create"),
            action_id="id_create_currency",
            hover_text="Create Currency",
        )
        return (action_new_currency,)


class CurrencyDetailView(MontrekDetailView):
    page_class = CurrencyPage
    tab = "tab_details"
    repository = CurrencyRepository
    title = "Details"

    @property
    def elements(self) -> tuple:
        return (
            StringTableElement(name="Name", attr="ccy_name"),
            StringTableElement(name="Code", attr="ccy_code"),
            FloatTableElement(name="FX Rate", attr="fx_rate"),
        )

    @property
    def actions(self) -> tuple:
        action_back = ActionElement(
            icon="chevron-left",
            link=reverse("currency"),
            action_id="id_back",
            hover_text="Back to Overview",
        )
        return (action_back,)


class CurrencyCreateView(MontrekCreateView):
    page_class = CurrencyAppPage
    title = "Overview Table"
    repository = CurrencyRepository
    form_class = CurrencyCreateForm
    success_url = "currency"
