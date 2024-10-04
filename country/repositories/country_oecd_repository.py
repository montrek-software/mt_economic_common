from django.utils import timezone
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
        self.add_satellite_fields_annotations(
            CountryOecdFxAnnualTSSatellite, ["year", "annual_fx_average"]
        )
        self.add_satellite_fields_annotations(
            CountryOecdInflationTSSatellite, ["year", "inflation"]
        )
        return self.build_queryset().filter(pk=self.session_data["pk"])


class CountryOecdFxAnnualRepository(MontrekRepository):
    hub_class = CountryHub

    def std_queryset(self, **kwargs):
        self.add_satellite_fields_annotations(CountryStaticSatellite, ["country_code"])
        self.add_last_ts_satellite_fields_annotations(
            CountryOecdFxAnnualTSSatellite,
            ["year", "annual_fx_average", "hub_entity_id"],
        )
        return self.build_queryset()


class CountryOecdInflationRepository(MontrekRepository):
    hub_class = CountryHub

    def std_queryset(self, **kwargs):
        self.add_satellite_fields_annotations(CountryStaticSatellite, ["country_code"])
        self.add_last_ts_satellite_fields_annotations(
            CountryOecdInflationTSSatellite,
            ["year", "inflation", "hub_entity_id"],
        )
        return self.build_queryset()


class CountryOecdApiRepository(MontrekRepository):
    hub_class = CountryHub

    def std_queryset(self, **kwargs):
        self.session_data["start_date"] = timezone.datetime.min
        self.session_data["end_date"] = timezone.datetime.max
        self.add_satellite_fields_annotations(
            CountryStaticSatellite, ["country_code_2"]
        )
        self.add_satellite_fields_annotations(
            CountryOecdFxAnnualTSSatellite,
            ["year", "annual_fx_average", "hub_entity_id"],
        )
        self.add_satellite_fields_annotations(
            CountryOecdInflationTSSatellite,
            ["inflation"],
        )
        return self.build_queryset()
