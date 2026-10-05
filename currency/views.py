from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from baseclasses.access import AccessKind
from baseclasses.dataclasses.view_classes import ActionElement
from baseclasses.views import MontrekListView
from baseclasses.views import MontrekDetailView
from baseclasses.views import MontrekCreateView
from baseclasses.views import MontrekTemplateView
from reporting.dataclasses.table_elements import (
    StringTableElement,
)
from mt_economic_common.currency.managers.currency_manager import (
    CurrencyManager,
    CurrencyDetailsManager,
)
from mt_economic_common.currency.managers.fx_rate_import_manager import (
    FxRateImportManager,
    FxRateImportRegistryManager,
)
from mt_economic_common.currency.managers.fx_rate_sources import FxRateSource
from mt_economic_common.currency.managers.currency_report_manager import (
    CurrencyReportManager,
)
from mt_economic_common.currency.pages import CurrencyAppPage
from mt_economic_common.currency.pages import CurrencyPage
from mt_economic_common.currency.forms import CurrencyCreateForm, FxRateImportForm
from mt_economic_common.currency.table_elements import FxRateTableElement
from reporting.views import MontrekReportView


class CurrencyOverview(MontrekListView):
    page_class = CurrencyAppPage
    tab = "tab_overview"
    title = "Overview Table"
    manager_class = CurrencyManager

    @property
    def actions(self) -> tuple:
        action_new_currency = ActionElement(
            icon="plus",
            link=reverse("currency_create"),
            action_id="id_create_currency",
            hover_text="Create Currency",
        )
        action_import_fx_rates = ActionElement(
            icon="upload",
            link=reverse("fx_rate_import"),
            action_id="id_import_fx_rates",
            hover_text="Import FX Rates",
        )
        return (action_new_currency, action_import_fx_rates)


class CurrencyDetailView(MontrekDetailView):
    page_class = CurrencyPage
    tab = "tab_details"
    manager_class = CurrencyDetailsManager
    title = "Details"

    @property
    def elements(self) -> tuple:
        return (
            StringTableElement(name="Name", attr="ccy_name"),
            StringTableElement(name="Code", attr="ccy_code"),
            StringTableElement(name="Symbol", attr="ccy_symbol"),
            FxRateTableElement(name="FX Rate", attr="fx_rate"),
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


class CurrencyReportView(MontrekReportView):
    page_class = CurrencyPage
    tab = "tab_report"
    title = "FX Rates"
    manager_class = CurrencyReportManager

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
    manager_class = CurrencyManager
    form_class = CurrencyCreateForm
    success_url = "currency"


class FxRateImportView(MontrekTemplateView):
    page_class = CurrencyAppPage
    tab = "tab_overview"
    title = "Import FX Rates"
    template_name = "fx_rate_import_form.html"
    manager_class = FxRateImportManager
    access_kind = AccessKind.CREATE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.import_form = FxRateImportForm()

    def get_template_context(self) -> dict:
        return {"import_form": self.import_form}

    def post(self, request, *args, **kwargs):
        self.import_form = FxRateImportForm(request.POST)
        if not self.import_form.is_valid():
            return self.render_to_response(self.get_context_data())
        result = self.manager.import_fx_rates(
            FxRateSource.from_label(self.import_form.cleaned_data["fx_source"]),
            self.import_form.cleaned_data["fx_value_date"],
        )
        if result:
            messages.info(request, self.manager.message)
        else:
            messages.error(request, self.manager.message)
        return HttpResponseRedirect(reverse("fx_rate_import_registry"))


class FxRateImportRegistryView(MontrekListView):
    page_class = CurrencyAppPage
    tab = "tab_fx_rate_import_registry"
    title = "FX Rate Imports"
    manager_class = FxRateImportRegistryManager

    @property
    def actions(self) -> tuple:
        action_import_fx_rates = ActionElement(
            icon="upload",
            link=reverse("fx_rate_import"),
            action_id="id_import_fx_rates",
            hover_text="Import FX Rates",
        )
        return (action_import_fx_rates,)
