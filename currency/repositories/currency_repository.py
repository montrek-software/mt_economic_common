from django.apps import apps
from django.db.models import QuerySet
from mt_economic_common.currency.models import CurrencyHub
from mt_economic_common.currency.models import CurrencyTimeSeriesSatellite
from mt_economic_common.currency.models import CurrencyStaticSatellite
from baseclasses.repositories.montrek_repository import MontrekRepository


def currency_time_series_satellite():
    return apps.get_model("currency", "CurrencyTimeSeriesSatellite")


class CurrencyRepository(MontrekRepository):
    hub_class = CurrencyHub
    latest_ts = True

    def set_annotations(self, **kwargs) -> QuerySet:
        self.add_satellite_fields_annotations(
            CurrencyTimeSeriesSatellite,
            ["fx_rate"],
        )
        self.add_satellite_fields_annotations(
            CurrencyStaticSatellite,
            ["ccy_name", "ccy_code", "ccy_symbol"],
        )


class CurrencyFxRateHistoryRepository(MontrekRepository):
    """All FX rates of one currency, ``pk`` being its hub value date id."""

    hub_class = CurrencyHub
    default_order_fields: tuple[str, ...] = ("-value_date",)

    def set_annotations(self, **kwargs) -> None:
        self.add_satellite_fields_annotations(
            CurrencyTimeSeriesSatellite,
            ["fx_rate"],
        )

    def receive(self) -> QuerySet:
        hub = self.get_hub_by_id(pk=self.session_data["pk"])
        return super().receive().filter(hub=hub)
