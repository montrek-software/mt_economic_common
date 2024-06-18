import sdmx
from api_upload.managers.request_manager import RequestManagerABC


class SdmxRequestManager(RequestManagerABC):
    def get_response(self, endpoint: str) -> dict | list:
        data_message = self._get_data_message(endpoint)
        return sdmx.to_pandas(data_message)

    def _get_data_message(self, endpoint: str) -> sdmx.message.DataMessage:
        return sdmx.read_url(self.get_endpoint_url(endpoint))
