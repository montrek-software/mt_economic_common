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


class CountryOecdTableRepository(MontrekRepository):
    hub_class = CountryHub

    def std_queryset(self, **kwargs):
        queryset = self.build_time_series_queryset(
            CountryOecdTSSatellite, self.reference_date
        )
        return queryset.filter(hub_entity_id=self.session_data["pk"])
