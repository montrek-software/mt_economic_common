import datetime

from baseclasses.forms import MontrekCreateForm
from django import forms

from mt_economic_common.currency.managers.fx_rate_sources import FxRateSource


class CurrencyCreateForm(MontrekCreateForm):
    class Meta:
        exclude = ["value_date", "fx_rate"]


def _yesterday() -> datetime.date:
    return datetime.date.today() - datetime.timedelta(days=1)


class FxRateImportForm(forms.Form):
    fx_source = forms.ChoiceField(
        label="Source",
        choices=FxRateSource.to_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    fx_value_date = forms.DateField(
        label="Value Date",
        initial=_yesterday,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
