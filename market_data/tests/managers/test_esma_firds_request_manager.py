from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlparse

from django.test import SimpleTestCase

from baseclasses.errors.montrek_user_error import MontrekError
from mt_economic_common.market_data.managers.esma_firds_request_manager import (
    EsmaFirdsRequestManager,
)
from mt_economic_common.market_data.utils import AssetTypes

REQUESTS_GET = "requesting.managers.request_manager.requests.get"

FIRDS_DOCS = [
    {
        "isin": "DE0007164600",
        "gnr_full_name": "SAP SE",
        "gnr_cfi_code": "ESVUFR",
        "gnr_notional_curr_code": "EUR",
        "lei": "529900D6BF99LW9R2E68",
        "mic": "XETR",
        "publication_date": "2026-10-01T00:00:00Z",
    },
    {
        "isin": "DE0007164600",
        "gnr_full_name": "SAP SE ORD",
        "gnr_cfi_code": "ESVUFR",
        "gnr_notional_curr_code": "EUR",
        "lei": "529900D6BF99LW9R2E68",
        "mic": "FRAA",
        "publication_date": "2026-10-03T00:00:00Z",
    },
    {
        "isin": "DE0001102580",
        "gnr_full_name": "DBR 0 15/02/32",
        "gnr_cfi_code": "DBFTFB",
        "gnr_notional_curr_code": "EUR",
        "lei": "529900AQBND3S6YJLY83",
        "mic": "SSOB",
        "publication_date": "2026-10-02T00:00:00Z",
        "bnd_maturity_date": "2032-02-15T00:00:00Z",
    },
]


def query_params(url: str) -> dict[str, list[str]]:
    return parse_qs(urlparse(url).query)


def mock_response(json_value: dict, status_code: int = 200) -> MagicMock:
    response = MagicMock()
    response.status_code = status_code
    response.ok = status_code < 400
    response.json.return_value = json_value
    return response


def fake_firds_get(url: str, *args, **kwargs) -> MagicMock:
    """Answer like the FIRDS Solr endpoint for the ISINs and page in the url."""
    params = query_params(url)
    query = params["q"][0]
    rows = int(params["rows"][0])
    start = int(params["start"][0])
    docs = [doc for doc in FIRDS_DOCS if doc["isin"] in query]
    return mock_response(
        {"response": {"numFound": len(docs), "docs": docs[start : start + rows]}}
    )


class MockEsmaFirdsRequestManager(EsmaFirdsRequestManager):
    pause_between_batches = 0
    sleep_time = 0


class TestEsmaFirdsRequestManager(SimpleTestCase):
    def setUp(self):
        self.manager = MockEsmaFirdsRequestManager({})

    @patch(REQUESTS_GET, side_effect=fake_firds_get)
    def test_get_data_as_df_returns_latest_record_per_isin(self, mock_get):
        df = self.manager.get_data_as_df(["de0007164600 ", "DE0001102580"])

        self.assertEqual(list(df.index), ["DE0001102580", "DE0007164600"])
        self.assertEqual(df.loc["DE0007164600", "name"], "SAP SE ORD")
        self.assertEqual(
            df.loc["DE0007164600", "asset_type"], AssetTypes.EQUITY.value.name
        )
        self.assertEqual(
            df.loc["DE0001102580", "asset_type"], AssetTypes.DEBT.value.name
        )
        self.assertEqual(df.loc["DE0001102580", "bnd_maturity_date"].year, 2032)
        self.assertNotIn("mic", df.columns)
        mock_get.assert_called_once()

    @patch(REQUESTS_GET, side_effect=fake_firds_get)
    def test_get_data_as_df_per_venue(self, mock_get):
        df = self.manager.get_data_as_df(["DE0007164600"], per_venue=True)

        self.assertEqual(len(df), 2)
        self.assertEqual(sorted(df["mic"]), ["FRAA", "XETR"])

    @patch(REQUESTS_GET, side_effect=fake_firds_get)
    def test_missing_and_invalid_isins_are_kept_as_empty_rows(self, mock_get):
        df = self.manager.get_data_as_df(["XX0000000000", "not-an-isin", ""])

        self.assertEqual(list(df.index), ["NOT-AN-ISIN", "XX0000000000"])
        self.assertTrue(df["name"].isna().all())
        query = query_params(mock_get.call_args.args[0])["q"][0]
        self.assertEqual(query, "isin:(XX0000000000)")

    @patch(REQUESTS_GET, side_effect=fake_firds_get)
    def test_no_valid_isins_make_no_request(self, mock_get):
        df = self.manager.get_data_as_df([])

        self.assertTrue(df.empty)
        mock_get.assert_not_called()

    @patch(REQUESTS_GET, side_effect=fake_firds_get)
    def test_isins_are_requested_in_batches(self, mock_get):
        self.manager.batch_size = 1

        df = self.manager.get_data_as_df(["DE0007164600", "DE0001102580"])

        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(len(df), 2)

    @patch(REQUESTS_GET, side_effect=fake_firds_get)
    def test_results_are_paged(self, mock_get):
        self.manager.page_size = 1

        df = self.manager.get_data_as_df(["DE0007164600"], per_venue=True)

        self.assertEqual(mock_get.call_count, 2)
        starts = [query_params(c.args[0])["start"] for c in mock_get.call_args_list]
        self.assertEqual(starts, [["0"], ["1"]])
        self.assertEqual(len(df), 2)

    @patch(REQUESTS_GET, return_value=mock_response({}, status_code=500))
    def test_failed_request_raises_montrek_error(self, mock_get):
        with self.assertRaisesMessage(MontrekError, "ESMA FIRDS request failed"):
            self.manager.get_data_as_df(["DE0007164600"])
