from django.db.models import QuerySet
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
    latest_ts = True

    def set_annotations(self, **kwargs):
        self.add_satellite_fields_annotations(CountryStaticSatellite, ["country_code"])
        self.add_satellite_fields_annotations(
            CountryOecdFxAnnualTSSatellite,
            ["year", "annual_fx_average"],
        )
        self.add_satellite_fields_annotations(
            CountryOecdInflationTSSatellite,
            ["inflation"],
        )


class CountryOecdTableRepository(MontrekRepository):
    hub_class = CountryHub

    def set_annotations(self, **kwargs):
        self.add_satellite_fields_annotations(
            CountryOecdFxAnnualTSSatellite, ["year", "annual_fx_average"]
        )
        self.add_satellite_fields_annotations(
            CountryOecdInflationTSSatellite, ["year", "inflation"]
        )

    def receive(self) -> QuerySet:
        hub = self.get_hub_by_id(pk=self.session_data.get("pk"))
        return super().receive().filter(hub=hub)


class CountryOecdFxAnnualRepository(MontrekRepository):
    hub_class = CountryHub
    latest_ts = True

    def set_annotations(self, **kwargs):
        self.add_satellite_fields_annotations(CountryStaticSatellite, ["country_code"])
        self.add_satellite_fields_annotations(
            CountryOecdFxAnnualTSSatellite,
            ["year", "annual_fx_average"],
        )


class CountryOecdInflationRepository(MontrekRepository):
    hub_class = CountryHub
    latest_ts = True

    def set_annotations(self, **kwargs):
        self.add_satellite_fields_annotations(CountryStaticSatellite, ["country_code"])
        self.add_satellite_fields_annotations(
            CountryOecdInflationTSSatellite,
            ["year", "inflation"],
        )


class CountryOecdApiRepository(MontrekRepository):
    hub_class = CountryHub

    def set_annotations(self, **kwargs):
        self.session_data["start_date"] = timezone.datetime.min
        self.session_data["end_date"] = timezone.datetime.max
        self.add_satellite_fields_annotations(
            CountryStaticSatellite, ["country_code_2"]
        )
        self.add_satellite_fields_annotations(
            CountryOecdFxAnnualTSSatellite,
            ["year", "annual_fx_average"],
        )
        self.add_satellite_fields_annotations(
            CountryOecdInflationTSSatellite,
            ["inflation"],
        )
