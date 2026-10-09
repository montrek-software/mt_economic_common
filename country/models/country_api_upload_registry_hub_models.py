from baseclasses.fields import HubForeignKey
from baseclasses.models import HubValueDate, MontrekHubABC


class CountryApiUploadRegistryHub(MontrekHubABC):
    pass


class CountryApiUploadRegistryHubValueDate(HubValueDate):
    hub = HubForeignKey(CountryApiUploadRegistryHub)
