"""
Fetch ESMA FIRDS reference data for a list of ISINs.

Uses the Solr backend behind the ESMA registers website (registers.esma.europa.eu).
The endpoint is public but not an officially documented API, so field names and
behaviour may change. For production, ingest the official FULINS/DLTINS bulk files.

FIRDS returns one record per ISIN *per trading venue (MIC)*, so we:
  1. fetch all current records for each ISIN (batched, OR-query),
  2. keep a "golden" row per ISIN (most recent publication),
  3. optionally keep the full per-venue table for inspection.
"""

import time
from collections.abc import Iterable, Iterator
from urllib.parse import urlencode

import pandas as pd

from baseclasses.errors.montrek_user_error import MontrekError
from mt_economic_common.market_data.utils import (
    ISIN_PATTERN,
    AssetTypes,
    normalize_identifiers,
)
from requesting.managers.request_manager import RequestJsonManager

# Fields confirmed on equity records; bond and derivative specific fields are
# kept automatically if present (see EXTRA_FIELD_PREFIXES).
CORE_FIELDS = {
    "isin": "isin",
    "gnr_full_name": "name",
    "gnr_short_name": "short_name",
    "gnr_cfi_code": "cfi_code",
    "gnr_notional_curr_code": "currency",
    "lei": "issuer_lei",
    "mic": "mic",
    "rca_mic": "relevant_authority_mic",
    "mrkt_trdng_start_date": "trading_start_date",
    "publication_date": "publication_date",
}
EXTRA_FIELD_PREFIXES = ("bnd_", "drv_", "dbt_")
DATE_COLUMNS = ("trading_start_date", "publication_date", "bnd_maturity_date")


class EsmaFirdsRequestManager(RequestJsonManager):
    base_url = "https://registers.esma.europa.eu/solr/esma_registers_firds/"
    batch_size = 50
    page_size = 1000
    pause_between_batches: float = 0.5

    def get_data_as_df(
        self, isins: Iterable[str], per_venue: bool = False
    ) -> pd.DataFrame:
        """
        Return FIRDS reference data for the given ISINs, indexed by ISIN.

        per_venue=False -> one row per ISIN (latest published record)
        per_venue=True  -> one row per ISIN x trading venue

        ISINs without a FIRDS record (or with an invalid format) appear as
        empty rows instead of being dropped silently.
        """
        requested = normalize_identifiers(isins)
        valid_isins = [isin for isin in requested if ISIN_PATTERN.match(isin)]

        records: list[dict] = []
        for batch_no, batch in enumerate(self._chunks(valid_isins)):
            if batch_no > 0:
                time.sleep(self.pause_between_batches)  # be polite to a public API
            records.extend(self._query_batch(batch))

        df = self._records_to_df(records, per_venue)

        missing = set(requested) - set(df["isin"])
        if missing:
            df = pd.concat(
                [df, pd.DataFrame({"isin": sorted(missing)})], ignore_index=True
            )
        return df.set_index("isin").sort_index()

    def _chunks(self, isins: list[str]) -> Iterator[list[str]]:
        for i in range(0, len(isins), self.batch_size):
            yield isins[i : i + self.batch_size]

    def _query_batch(self, isins: list[str]) -> list[dict]:
        """Fetch all current FIRDS records for a batch of ISINs, page by page."""
        query = "isin:(" + " OR ".join(isins) + ")"
        docs: list[dict] = []
        start = 0
        while True:
            params = {
                "q": query,
                # only the current version of each record
                "fq": ["latest_received_flag:1", "type_s:parent"],
                "wt": "json",
                "rows": self.page_size,
                "start": start,
            }
            response = self.get_response(f"select?{urlencode(params, doseq=True)}")
            if not isinstance(response, dict) or "response" not in response:
                raise MontrekError(f"ESMA FIRDS request failed: {self.message}")
            body = response["response"]
            docs.extend(body["docs"])
            start += self.page_size
            if start >= body["numFound"]:
                return docs

    @staticmethod
    def _records_to_df(records: list[dict], per_venue: bool) -> pd.DataFrame:
        if not records:
            return pd.DataFrame(columns=[*CORE_FIELDS.values(), "asset_type"])

        raw = pd.DataFrame.from_records(records)
        extra = [c for c in raw.columns if c.startswith(EXTRA_FIELD_PREFIXES)]
        cols = [c for c in CORE_FIELDS if c in raw.columns] + extra
        df = raw[cols].rename(columns=CORE_FIELDS)

        for col in DATE_COLUMNS:
            if col in df:
                df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)

        asset_types = {m.value.cfi_prefix: m.value.name for m in AssetTypes}
        df["asset_type"] = df["cfi_code"].str[0].map(asset_types)

        # Never let an attribute-less record represent an ISIN
        df = df.dropna(subset=["name", "cfi_code"], how="all")

        if not per_venue:
            df = (
                df.sort_values("publication_date", ascending=False)
                .drop_duplicates("isin", keep="first")
                .drop(columns=["mic"], errors="ignore")
            )
        return df
