from baseclasses.fields import HubForeignKey
from baseclasses.models import HubValueDate, MontrekHubABC


class CountryApiCredentialsHub(MontrekHubABC):
    pass


class CountryApiCredentialsHubValueDate(HubValueDate):
    hub = HubForeignKey(CountryApiCredentialsHub)
