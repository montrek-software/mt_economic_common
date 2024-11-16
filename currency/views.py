from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from baseclasses.dataclasses.view_classes import ActionElement
from baseclasses.views import MontrekListView
from baseclasses.views import MontrekDetailView
from baseclasses.views import MontrekCreateView
from reporting.dataclasses.table_elements import (
    StringTableElement,
    FloatTableElement,
)
from mt_economic_common.currency.managers.currency_manager import (
    CurrencyManager,
    CurrencyDetailsManager,
    YahooFxUploadManager,
)
from mt_economic_common.currency.pages import CurrencyAppPage
from mt_economic_common.currency.pages import CurrencyPage
from mt_economic_common.currency.forms import CurrencyCreateForm

# Create your views here.


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
        action_yahoo_upload = ActionElement(
            icon="upload",
            link=reverse("upload_yahoo_fx_rates"),
            action_id="id_upload_yahoo_fx_rates",
            hover_text="Yahoo FX Rates Upload",
        )
        return (action_new_currency, action_yahoo_upload)


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
    manager_class = CurrencyManager
    form_class = CurrencyCreateForm
    success_url = "currency"


def upload_yahoo_fx_rates(request):
    yahoo_manager = YahooFxUploadManager(session_data={"user_id": request.user.id})
    yahoo_manager.update_fx_rates(
        (timezone.datetime.now() - timezone.timedelta(days=1)).date()
    )
    return HttpResponseRedirect(reverse("currency"))
