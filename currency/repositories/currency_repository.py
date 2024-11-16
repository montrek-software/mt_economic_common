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
