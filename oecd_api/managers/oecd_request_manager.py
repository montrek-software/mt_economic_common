import pandas as pd
from api_upload.managers.request_manager import RequestJsonManager
from mt_economic_common.oecd_api.utils.sdmx_json_reader import SdmxJsonReader
from mt_economic_common.country.repositories.country_repository import CountryRepository


class OecdRequestManager(RequestJsonManager):
    base_url = "https://sdmx.oecd.org/public/rest/data/"
    json_reader = SdmxJsonReader()

    def get_endpoint_url(self, endpoint: str) -> str:
        return super().get_endpoint_url(endpoint) + "&format=jsondata"
