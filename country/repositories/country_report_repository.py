from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_economic_common.country.models import CountryHub, CountryStaticSatellite


class CountryReportRepository(MontrekRepository):
    hub_class = CountryHub

    def set_annotations(self):
        self.add_satellite_fields_annotations(
            CountryStaticSatellite,
            [
                "country_name",
            ],
        )
