import os
import json

from mt_economic_common.country.managers.country_manager import (
    RestCountriesUploadManager,
)
from mt_economic_common.country.managers.country_request_manager import (
    RestCountriesRequestManager,
)
from mt_economic_common.country.managers.country_upload_processors import (
    RestCountriesUploadProcessor,
)
from mt_economic_common.country.views import UploadCountryApiView


class MockRestCountriesRequestManager(RestCountriesRequestManager):
    def get_response(self, endpoint: str) -> dict | list:
        with open(
            os.path.join(
                os.path.dirname(__file__), "test_data/rest_countries_example.json"
            )
        ) as f:
            return json.loads(f.read())


class MockRestCountriesUploadProcessor(RestCountriesUploadProcessor):
    request_manager_class = MockRestCountriesRequestManager


class MockRestCountriesUploadManager(RestCountriesUploadManager):
    processor_class = MockRestCountriesUploadProcessor


class MockUploadCountryApiView(UploadCountryApiView):
    manager_class = MockRestCountriesUploadManager
