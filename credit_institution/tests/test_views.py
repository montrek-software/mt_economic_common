from django.test import TestCase
from mt_economic_common.credit_institution.tests.factories.credit_institution_factories import (
    CreditInstitutionStaticSatelliteFactory,
)
from mt_economic_common.country.tests.factories.country_factories import (
    CountryStaticSatelliteFactory,
)
from mt_economic_common.credit_institution import views
from testing.test_cases import view_test_cases as vtc


class TestCreditInstitutionOverview(vtc.MontrekListViewTestCase):
    viewname = "credit_institution"
    view_class = views.CreditInstitutionOverview
    expected_no_of_rows = 5

    def build_factories(self):
        CreditInstitutionStaticSatelliteFactory.create_batch(5)


class TestCreditInstitutionDetailView(vtc.MontrekDetailViewTestCase):
    viewname = "credit_institution_details"
    view_class = views.CreditIntitutionDetailView

    def build_factories(self):
        self.credit_institution = CreditInstitutionStaticSatelliteFactory()

    def url_kwargs(self) -> dict:
        return {"pk": self.credit_institution.hub_entity.pk}


class TestCreditInstitutionCreateView(vtc.MontrekCreateViewTestCase):
    viewname = "credit_institution_create"
    view_class = views.CreditInstitutionCreate

    def creation_data(self) -> dict:
        return {
            "credit_institution_name": "Test Credit Institution",
            "credit_institution_bic": "TESTBIC",
            "account_upload_method": "none",
        }
