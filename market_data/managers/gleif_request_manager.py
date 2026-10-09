"""
Fetch issuer data from the GLEIF API for a list of LEIs.

GLEIF API: https://api.gleif.org/api/v1 (free, no API key, JSON:API format,
rate limited to 60 requests per minute).

  - get_data_as_df(leis)               -> one row per LEI: legal name, addresses,
                                          legal form, jurisdiction, status, BIC, ...
  - get_data_as_df(leis, parents=True) -> adds direct and ultimate parent LEI + name
  - get_leis_for_isins(isins)          -> ISIN -> LEI lookup via GLEIF's ISIN mapping
                                          (useful as a fallback when FIRDS has no record)
"""

import time
from collections.abc import Iterable, Iterator
from http import HTTPStatus
from typing import Any
from urllib.parse import urlencode

import pandas as pd
import requests

from baseclasses.errors.montrek_user_error import MontrekError
from mt_economic_common.market_data.utils import (
    ISIN_PATTERN,
    LEI_PATTERN,
    normalize_identifiers,
)
from requesting.managers.request_manager import RequestJsonManager

DATE_COLUMNS = ("creation_date", "last_update", "next_renewal")
PARENT_KINDS = (
    ("direct-parent", "direct_parent"),
    ("ultimate-parent", "ultimate_parent"),
)


def _address(address: dict | None) -> dict[str, Any]:
    address = address or {}
    return {
        "street": ", ".join(address.get("addressLines") or []),
        "postal_code": address.get("postalCode"),
        "city": address.get("city"),
        "region": address.get("region"),
        "country": address.get("country"),
    }


def flatten_lei_record(record: dict) -> dict[str, Any]:
    """Flatten one GLEIF lei-record into a flat dict."""
    attributes = record["attributes"]
    entity = attributes["entity"]
    registration = attributes["registration"]
    legal_form = entity.get("legalForm") or {}
    legal_address = _address(entity.get("legalAddress"))
    hq_address = _address(entity.get("headquartersAddress"))
    return {
        "lei": attributes["lei"],
        "legal_name": (entity.get("legalName") or {}).get("name"),
        "other_names": "; ".join(n["name"] for n in entity.get("otherNames") or []),
        "legal_form_elf": legal_form.get("id"),  # ISO 20275 ELF code, e.g. SGST
        "legal_form_other": legal_form.get("other"),
        "jurisdiction": entity.get("jurisdiction"),
        "category": entity.get("category"),  # GENERAL, FUND, BRANCH, ...
        "entity_status": entity.get("status"),  # ACTIVE / INACTIVE
        "creation_date": entity.get("creationDate"),
        "registered_as": entity.get("registeredAs"),  # e.g. HRB number
        **{f"legal_{k}": v for k, v in legal_address.items()},
        **{f"hq_{k}": v for k, v in hq_address.items()},
        "registration_status": registration.get("status"),  # ISSUED, LAPSED, ...
        "last_update": registration.get("lastUpdateDate"),
        "next_renewal": registration.get("nextRenewalDate"),
        "bic": "; ".join(attributes.get("bic") or []),
    }


LEI_RECORD_COLUMNS = list(
    flatten_lei_record({"attributes": {"lei": None, "entity": {}, "registration": {}}})
)


class GleifRequestManager(RequestJsonManager):
    base_url = "https://api.gleif.org/api/v1/"
    page_size = 200  # max page size of the GLEIF API
    pause_between_requests: float = 0.2
    rate_limit_backoff: float = 1

    def get_data_as_df(
        self, leis: Iterable[str], parents: bool = False
    ) -> pd.DataFrame:
        """
        Return GLEIF issuer data, one row per LEI, indexed by LEI.

        parents=True adds direct and ultimate parent LEI and name. This costs two
        extra requests per LEI - fine for hundreds, slow for thousands. For bulk
        use, ingest the GLEIF Level-2 relationship file instead.

        LEIs without a GLEIF record (or with an invalid format) appear as empty
        rows instead of being dropped silently.
        """
        requested = normalize_identifiers(leis)
        valid_leis = [lei for lei in requested if LEI_PATTERN.match(lei)]

        rows: list[dict] = []
        for batch in self._chunks(valid_leis):
            params = {"filter[lei]": ",".join(batch), "page[size]": self.page_size}
            body = self._get_json(f"lei-records?{urlencode(params)}")
            if body:
                rows.extend(flatten_lei_record(rec) for rec in body["data"])

        df = pd.DataFrame(rows, columns=LEI_RECORD_COLUMNS)

        if parents:
            for kind, prefix in PARENT_KINDS:
                found = [self._get_parent(lei, kind) for lei in df["lei"]]
                df[f"{prefix}_lei"] = [parent_lei for parent_lei, _ in found]
                df[f"{prefix}_name"] = [parent_name for _, parent_name in found]

        for col in DATE_COLUMNS:
            df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)

        missing = set(requested) - set(df["lei"])
        if missing:
            df = pd.concat(
                [df, pd.DataFrame({"lei": sorted(missing)})], ignore_index=True
            )
        return df.set_index("lei").sort_index()

    def get_leis_for_isins(self, isins: Iterable[str]) -> pd.DataFrame:
        """
        ISIN -> LEI via GLEIF's ISIN mapping (sourced from ANNA / the numbering
        agencies). Coverage is good for listed shares and bonds but not complete.
        One request per ISIN; unknown or invalid ISINs get empty values.
        """
        rows = []
        for isin in normalize_identifiers(isins):
            data = []
            if ISIN_PATTERN.match(isin):
                body = self._get_json(
                    f"lei-records?{urlencode({'filter[isin]': isin})}"
                )
                data = (body or {}).get("data") or []
            record = flatten_lei_record(data[0]) if data else {}
            rows.append(
                {
                    "isin": isin,
                    "lei": record.get("lei"),
                    "legal_name": record.get("legal_name"),
                }
            )
        return pd.DataFrame(rows, columns=["isin", "lei", "legal_name"]).set_index(
            "isin"
        )

    def get_request(
        self, endpoint_url: str, headers: dict[str, Any]
    ) -> requests.models.Response:
        """Retry with exponential backoff while GLEIF answers 429 Too Many Requests."""
        for attempt in range(self.no_of_retries):
            response = super().get_request(endpoint_url, headers)
            if response.status_code != HTTPStatus.TOO_MANY_REQUESTS:
                return response
            time.sleep(self.rate_limit_backoff * 2**attempt)
        return response

    def get_headers(self) -> dict[str, Any]:
        headers = super().get_headers()
        headers["Accept"] = "application/vnd.api+json"
        return headers

    def _chunks(self, leis: list[str]) -> Iterator[list[str]]:
        for i in range(0, len(leis), self.page_size):
            yield leis[i : i + self.page_size]

    def _get_json(self, endpoint: str) -> dict | None:
        """GET a GLEIF resource. Returns None on 404, raises on any other failure."""
        response = self.get_response(endpoint)
        time.sleep(self.pause_between_requests)  # be polite to a public API
        if self.status_code == HTTPStatus.NOT_FOUND:
            return None
        if not isinstance(response, dict) or "data" not in response:
            raise MontrekError(f"GLEIF request failed: {self.message}")
        return response

    def _get_parent(self, lei: str, kind: str) -> tuple[str | None, str | None]:
        """kind = 'direct-parent' or 'ultimate-parent'."""
        body = self._get_json(f"lei-records/{lei}/{kind}")
        if not body or not body["data"]:
            return None, None  # no parent reported, or a reporting exception
        attributes = body["data"]["attributes"]
        return attributes["lei"], attributes["entity"]["legalName"]["name"]
