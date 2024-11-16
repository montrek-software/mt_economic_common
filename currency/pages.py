from django.urls import reverse

from baseclasses.dataclasses.view_classes import TabElement, ActionElement
from baseclasses.pages import MontrekPage
from mt_economic_common.currency.repositories.currency_repository import (
    CurrencyRepository,
)


class CurrencyAppPage(MontrekPage):
    page_title = "Currencies"
    show_date_range_selector = True

    def get_tabs(self):
        return [
            TabElement(
                html_id="tab_overview",
                name="Overview",
                link=reverse("currency"),
            ),
        ]


class CurrencyPage(MontrekPage):
    show_date_range_selector = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "pk" not in kwargs:
            raise ValueError("CurrencyPage needs pk specified in url!")
        self.obj = CurrencyRepository().receive().get(pk=kwargs["pk"])
        self.page_title = self.obj.ccy_name

    def get_tabs(self):
        details_tab = TabElement(
            name="Details",
            link=reverse("currency_details", args=[self.obj.id]),
            html_id="tab_details",
        )
        return [details_tab]
