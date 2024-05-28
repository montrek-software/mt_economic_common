import pandas as pd
from api_upload.managers.request_manager import RequestManager
from mt_economic_common.oecd_api.utils.sdmx_json_reader import SdmxJsonReader


class OecdRequestManager(RequestManager):
    base_url = "https://sdmx.oecd.org/public/rest/data/"

    def get_endpoint_url(self, endpoint: str) -> str:
        return super().get_endpoint_url(endpoint) + "&format=jsondata"

    def get_average_annual_fx_rates(self) -> pd.DataFrame:
        test_json = self.get_json(
            "OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE4,1.0/A....EXC_A.......?startPeriod=2000"
        )
        reader = SdmxJsonReader(json_data=test_json)
        result_df = reader.to_data_frame()
        return result_df
