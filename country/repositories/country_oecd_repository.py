from django.db.models import OuterRef, Subquery
from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_economic_common.country.models import (
    CountryHub,
    CountryOecdFxAnnualTSSatellite,
    CountryOecdInflationTSSatellite,
    CountryStaticSatellite,
)


class CountryOecdRepository(MontrekRepository):
    hub_class = CountryHub

    def std_queryset(self, **kwargs):
        self.add_satellite_fields_annotations(CountryStaticSatellite, ["country_code"])
        self.add_last_ts_satellite_fields_annotations(
            CountryOecdFxAnnualTSSatellite,
            ["year", "annual_fx_average", "hub_entity_id"],
        )
        self.add_last_ts_satellite_fields_annotations(
            CountryOecdInflationTSSatellite,
            ["inflation"],
        )
        return self.build_queryset()


class CountryOecdTableRepository(MontrekRepository):
    hub_class = CountryHub

    def std_queryset(self, **kwargs):
        queryset = self.build_time_series_queryset(
            CountryOecdFxAnnualTSSatellite, self.reference_date
        )
        queryset = queryset.annotate(
            inflation=Subquery(
                self.build_time_series_queryset(
                    CountryOecdInflationTSSatellite, self.reference_date
                )
                .filter(year=OuterRef("year"), hub_entity=OuterRef("hub_entity"))
                .values("inflation")
            )
        )
        return queryset.filter(hub_entity_id=self.session_data["pk"])
