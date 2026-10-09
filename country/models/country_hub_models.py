from baseclasses.fields import HubForeignKey
from baseclasses.models import HubValueDate, MontrekHubABC, MontrekManyToManyLinkABC
from django.db import models


class CountryHub(MontrekHubABC):
    link_country_currency = models.ManyToManyField(
        "currency.CurrencyHub",
        related_name="link_currency_country",
        through="LinkCountryCurrency",
    )


class CountryHubValueDate(HubValueDate):
    hub = HubForeignKey(CountryHub)


class LinkCountryCurrency(MontrekManyToManyLinkABC):
    hub_in = models.ForeignKey(
        "country.CountryHub",
        on_delete=models.CASCADE,
    )
    hub_out = models.ForeignKey("currency.CurrencyHub", on_delete=models.CASCADE)
