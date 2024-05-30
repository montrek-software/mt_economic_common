from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_economic_common.country.models import (
    CountryHub,
    CountryOecdTSSatellite,
    CountryStaticSatellite,
)


class CountryOecdRepository(MontrekRepository):
    hub_class = CountryHub

    def std_queryset(self, **kwargs):
        self.add_satellite_fields_annotations(CountryStaticSatellite, ["country_code"])
        self.add_last_ts_satellite_fields_annotations(
            CountryOecdTSSatellite, ["year", "annual_fx_average", "hub_entity_id"]
        )
        return self.build_queryset()

    def get_country_oecd_ts(self, country_id: int):
        return self.build_time_series_queryset(
            CountryOecdTSSatellite, self.reference_date
        ).filter(hub_entity_id=country_id)
