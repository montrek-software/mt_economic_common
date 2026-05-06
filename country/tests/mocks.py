import os
import json
from pathlib import Path

import sdmx

from mt_economic_common.country.managers.country_manager import (
    RestCountriesUploadManager,
)
from mt_economic_common.country.managers.country_oecd_manager import (
    CountryOecdAnnualFxUploadManager,
)
from mt_economic_common.country.managers.country_request_manager import (
    RestCountriesRequestManager,
)
from mt_economic_common.country.managers.country_upload_processors import (
    OecdAnnualFxUploadProcessor,
    RestCountriesUploadProcessor,
)
from mt_economic_common.country.views import (
    UploadCountryApiView,
    UploadOecdCountryDataView,
)
from mt_economic_common.sdmx_api.managers.sdmx_request_manager import (
    OecdSdmxRequestManager,
)


class MockRestCountriesRequestManager(RestCountriesRequestManager):
    def get_response(self, endpoint: str) -> dict | list:
        self.status_code = 200
        with open(
            os.path.join(
                os.path.dirname(__file__), "test_data/rest_countries_example.json"
            )
        ) as f:
            return json.loads(f.read())


class MockRestCountriesUploadProcessor(RestCountriesUploadProcessor):
    request_manager_class = MockRestCountriesRequestManager
    country_locality_request_manager_class = MockRestCountriesRequestManager


class MockRestCountriesUploadManager(RestCountriesUploadManager):
    processor_class = MockRestCountriesUploadProcessor


class MockUploadCountryApiView(UploadCountryApiView):
    manager_class = MockRestCountriesUploadManager


class MockOecdSdmxRequestManager(OecdSdmxRequestManager):
    def load_sdmx_fixture(self, name: str):
        return sdmx.read_sdmx(Path(__file__).parent / "test_data" / name)

    def _get_data_message(self, endpoint: str) -> sdmx.message.DataMessage:
        return self.load_sdmx_fixture("fx_annual_example.xml")


class MockOecdAnnualFxUploadProcessor(OecdAnnualFxUploadProcessor):
    request_manager_class = MockOecdSdmxRequestManager


class MockCountryOecdAnnualFxUploadManager(CountryOecdAnnualFxUploadManager):
    processor_class = MockOecdAnnualFxUploadProcessor


class MockUploadOECDCountryDataView(UploadOecdCountryDataView):
    manager_class = MockCountryOecdAnnualFxUploadManager
