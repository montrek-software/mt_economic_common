from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlparse

from django.test import SimpleTestCase

from baseclasses.errors.montrek_user_error import MontrekError
from mt_economic_common.market_data.managers.gleif_request_manager import (
    GleifRequestManager,
)

REQUESTS_GET = "requesting.managers.request_manager.requests.get"

SAP_LEI = "529900D6BF99LW9R2E68"
SUBSIDIARY_LEI = "529900AAAAAAAAAAAA11"
UNKNOWN_LEI = "529900ZZZZZZZZZZZZ99"


def lei_record(lei: str, name: str, **entity) -> dict:
    return {
        "type": "lei-records",
        "attributes": {
            "lei": lei,
            "entity": {
                "legalName": {"name": name},
                "legalForm": {"id": "SGST", "other": None},
                "legalAddress": {
                    "addressLines": ["Dietmar-Hopp-Allee 16"],
                    "postalCode": "69190",
                    "city": "Walldorf",
                    "country": "DE",
                },
                "jurisdiction": "DE",
                "category": "GENERAL",
                "status": "ACTIVE",
                "creationDate": "1972-04-01T00:00:00Z",
                **entity,
            },
            "registration": {
                "status": "ISSUED",
                "lastUpdateDate": "2026-05-01T00:00:00Z",
                "nextRenewalDate": "2027-05-01T00:00:00Z",
            },
            "bic": ["SAPXDEFFXXX"],
        },
    }


LEI_RECORDS = {
    SAP_LEI: lei_record(SAP_LEI, "SAP SE"),
    SUBSIDIARY_LEI: lei_record(SUBSIDIARY_LEI, "SAP Subsidiary GmbH"),
}
PARENTS = {SUBSIDIARY_LEI: SAP_LEI}
ISIN_TO_LEI = {"DE0007164600": SAP_LEI}


def mock_response(json_value: dict, status_code: int = 200) -> MagicMock:
    response = MagicMock()
    response.status_code = status_code
    response.ok = status_code < 400
    response.json.return_value = json_value
    return response


NOT_FOUND = mock_response({"errors": [{"status": "404"}]}, status_code=404)


def fake_gleif_get(url: str, *args, **kwargs) -> MagicMock:
    """Answer like the GLEIF API for lei-records, ISIN filters and parents."""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    path = parsed.path.removeprefix("/api/v1/lei-records")
    if path.endswith(("/direct-parent", "/ultimate-parent")):
        parent_lei = PARENTS.get(path.split("/")[1])
        if parent_lei is None:
            return NOT_FOUND
        return mock_response({"data": LEI_RECORDS[parent_lei]})
    if "filter[lei]" in params:
        leis = params["filter[lei]"][0].split(",")
        return mock_response(
            {"data": [LEI_RECORDS[lei] for lei in leis if lei in LEI_RECORDS]}
        )
    lei = ISIN_TO_LEI.get(params["filter[isin]"][0])
    return mock_response({"data": [LEI_RECORDS[lei]] if lei else []})


class MockGleifRequestManager(GleifRequestManager):
    pause_between_requests = 0
    rate_limit_backoff = 0
    sleep_time = 0


class TestGleifRequestManager(SimpleTestCase):
    def setUp(self):
        self.manager = MockGleifRequestManager({})

    @patch(REQUESTS_GET, side_effect=fake_gleif_get)
    def test_get_data_as_df(self, mock_get):
        df = self.manager.get_data_as_df([f" {SAP_LEI.lower()}", UNKNOWN_LEI, "XYZ"])

        self.assertEqual(list(df.index), sorted([SAP_LEI, UNKNOWN_LEI, "XYZ"]))
        sap = df.loc[SAP_LEI]
        self.assertEqual(sap["legal_name"], "SAP SE")
        self.assertEqual(sap["legal_form_elf"], "SGST")
        self.assertEqual(sap["legal_street"], "Dietmar-Hopp-Allee 16")
        self.assertEqual(sap["legal_city"], "Walldorf")
        self.assertEqual(sap["bic"], "SAPXDEFFXXX")
        self.assertEqual(sap["creation_date"].year, 1972)
        self.assertTrue(df.loc[[UNKNOWN_LEI, "XYZ"], "legal_name"].isna().all())
        self.assertNotIn("direct_parent_lei", df.columns)
        mock_get.assert_called_once()
        self.assertEqual(
            mock_get.call_args.kwargs["headers"]["Accept"], "application/vnd.api+json"
        )

    @patch(REQUESTS_GET, side_effect=fake_gleif_get)
    def test_get_data_as_df_with_parents(self, mock_get):
        df = self.manager.get_data_as_df([SAP_LEI, SUBSIDIARY_LEI], parents=True)

        self.assertEqual(df.loc[SUBSIDIARY_LEI, "direct_parent_lei"], SAP_LEI)
        self.assertEqual(df.loc[SUBSIDIARY_LEI, "ultimate_parent_name"], "SAP SE")
        self.assertIsNone(df.loc[SAP_LEI, "direct_parent_lei"])
        self.assertIsNone(df.loc[SAP_LEI, "ultimate_parent_name"])
        # one batch request plus two parent requests per LEI
        self.assertEqual(mock_get.call_count, 5)

    @patch(REQUESTS_GET, side_effect=fake_gleif_get)
    def test_no_valid_leis_make_no_request(self, mock_get):
        df = self.manager.get_data_as_df(["", "not-a-lei"])

        self.assertEqual(list(df.index), ["NOT-A-LEI"])
        self.assertIn("legal_name", df.columns)
        mock_get.assert_not_called()

    @patch(REQUESTS_GET, side_effect=fake_gleif_get)
    def test_leis_are_requested_in_batches(self, mock_get):
        self.manager.page_size = 1

        df = self.manager.get_data_as_df([SAP_LEI, SUBSIDIARY_LEI])

        self.assertEqual(mock_get.call_count, 2)
        self.assertTrue(df["legal_name"].notna().all())

    @patch(REQUESTS_GET, side_effect=fake_gleif_get)
    def test_get_leis_for_isins(self, mock_get):
        df = self.manager.get_leis_for_isins(
            ["DE0007164600", "XX0000000000", "not-an-isin"]
        )

        self.assertEqual(df.loc["DE0007164600", "lei"], SAP_LEI)
        self.assertEqual(df.loc["DE0007164600", "legal_name"], "SAP SE")
        self.assertIsNone(df.loc["XX0000000000", "lei"])
        self.assertIsNone(df.loc["NOT-AN-ISIN", "lei"])
        self.assertEqual(mock_get.call_count, 2)

    @patch(REQUESTS_GET)
    def test_rate_limited_requests_are_retried(self, mock_get):
        mock_get.side_effect = [
            mock_response({}, status_code=429),
            mock_response({}, status_code=429),
            fake_gleif_get(
                f"https://api.gleif.org/api/v1/lei-records?filter[lei]={SAP_LEI}"
            ),
        ]

        df = self.manager.get_data_as_df([SAP_LEI])

        self.assertEqual(mock_get.call_count, 3)
        self.assertEqual(df.loc[SAP_LEI, "legal_name"], "SAP SE")

    @patch(REQUESTS_GET, return_value=mock_response({}, status_code=429))
    def test_persistent_rate_limit_raises_montrek_error(self, mock_get):
        with self.assertRaisesMessage(MontrekError, "GLEIF request failed"):
            self.manager.get_data_as_df([SAP_LEI])
        self.assertEqual(mock_get.call_count, self.manager.no_of_retries)

    @patch(REQUESTS_GET, return_value=mock_response({}, status_code=500))
    def test_failed_request_raises_montrek_error(self, mock_get):
        with self.assertRaisesMessage(MontrekError, "GLEIF request failed"):
            self.manager.get_data_as_df([SAP_LEI])
