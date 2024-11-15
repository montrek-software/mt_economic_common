from django.db import models
from baseclasses import models as baseclass_models
from baseclasses.fields import HubForeignKey

# Create your models here.


class CurrencyHub(baseclass_models.MontrekHubABC):
    pass


class CurrencyHubValueDate(baseclass_models.HubValueDate):
    hub = HubForeignKey(CurrencyHub)


class CurrencyStaticSatellite(baseclass_models.MontrekSatelliteABC):
    hub_entity = models.ForeignKey(
        CurrencyHub, on_delete=models.CASCADE, related_name="currency_static_satellites"
    )
    ccy_name = models.CharField(max_length=50)
    ccy_code = models.CharField(max_length=3)
    ccy_symbol = models.CharField(max_length=15, null=True, blank=True)
    identifier_fields = ["ccy_code"]

    def __str__(self):
        return f"{self.ccy_name} ({self.ccy_code})"


class CurrencyTimeSeriesSatellite(baseclass_models.MontrekTimeSeriesSatelliteABC):
    hub_value_date = models.ForeignKey(
        CurrencyHubValueDate,
        on_delete=models.CASCADE,
        related_name="currency_time_series_satellites",
    )
    fx_rate = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    identifier_fields = ["value_date", "hub_entity"]
