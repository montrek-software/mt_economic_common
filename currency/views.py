from django.shortcuts import render
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


class CurrencyDetailView(MontrekDetailView):
    page_class = CurrencyPage
    tab = "tab_details"
    repository = CurrencyRepository
    title = "Details"

    @property
    def elements(self) -> dict:
        return (
            StringTableElement(name="Name", attr="ccy_name"),
            StringTableElement(name="Code", attr="ccy_code"),
            FloatTableElement(name="FX Rate", attr="fx_rate"),
        )


class CurrencyCreateView(MontrekCreateView):
    page_class = CurrencyAppPage
    title = "Overview Table"
    repository = CurrencyRepository
    form_class = CurrencyCreateForm
    success_url = "currency"
