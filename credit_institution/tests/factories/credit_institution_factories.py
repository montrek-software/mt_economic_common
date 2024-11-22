import factory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekHubFactory,
    MontrekSatelliteFactory,
)


class CreditInstitutionHubFactory(MontrekHubFactory):
    class Meta:
        model = "credit_institution.CreditInstitutionHub"


class CreditInstitutionStaticSatelliteFactory(MontrekSatelliteFactory):
    class Meta:
        model = "credit_institution.CreditInstitutionStaticSatellite"

    hub_entity = factory.SubFactory(CreditInstitutionHubFactory)
    credit_institution_name = factory.Faker("company")
