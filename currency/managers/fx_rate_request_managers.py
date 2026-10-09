from requesting.managers.request_manager import RequestJsonManager


class FrankfurterRequestManager(RequestJsonManager):
    """ECB reference rates, see https://frankfurter.dev."""

    base_url = "https://api.frankfurter.app/"
