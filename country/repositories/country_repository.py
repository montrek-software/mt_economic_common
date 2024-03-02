from django.utils import timezone
from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_economic_common.country.models import CountryHub, CountryStaticSatellite


class CountryRepository(MontrekRepository):
    hub_class = CountryHub

    def std_queryset(self):
        self.add_satellite_fields_annotations(
            CountryStaticSatellite, ["country_name", "country_code"]
        )
        return self.build_queryset()
