from api_upload.managers.request_manager import RequestManager


class OecdRequestManager(RequestManager):
    base_url = "https://sdmx.oecd.org/public/rest/data/"

    def get_endpoint_url(self, endpoint: str) -> str:
        return super().get_endpoint_url(endpoint) + "&format=jsondata"
