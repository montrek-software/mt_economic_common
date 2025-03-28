from django.conf import settings
import sdmx
import pandas as pd
from requesting.managers.request_manager import RequestManagerABC


class SdmxRequestManager(RequestManagerABC):
    def get_response(self, endpoint: str) -> pd.DataFrame:
        try:
            data_message = self._get_data_message(endpoint)
            response_df = sdmx.to_pandas(data_message)
        except Exception as e:
            if settings.IS_TEST_RUN:
                raise e
            self.message = (
                f"Error raised during object creation: {e.__class__.__name__}: {e}"
            )
            return pd.DataFrame()
        self.status_code = 1
        return response_df

    def _get_data_message(self, endpoint: str) -> sdmx.message.DataMessage:
        return sdmx.read_url(self.get_endpoint_url(endpoint))


class OecdSdmxRequestManager(SdmxRequestManager):
    base_url = "https://sdmx.oecd.org/public/rest/data/"
