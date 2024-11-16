from mt_economic_common.credit_institution.models import (
    CreditInstitutionHub,
    CreditInstitutionStaticSatellite,
    LinkCreditInstitutionCountry,
)
from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_economic_common.country.models import CountryStaticSatellite


class CreditInstitutionRepository(MontrekRepository):
    hub_class = CreditInstitutionHub

    def set_annotations(self, **kwargs):
        self.add_satellite_fields_annotations(
            CreditInstitutionStaticSatellite,
            [
                "credit_institution_name",
                "credit_institution_bic",
                "account_upload_method",
            ],
        )
        self.add_linked_satellites_field_annotations(
            CountryStaticSatellite,
            LinkCreditInstitutionCountry,
            [
                "country_name",
                "hub_entity_id",
            ],
        )
        self.rename_field("hub_entity_id", "country_id")
