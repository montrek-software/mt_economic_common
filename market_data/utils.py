import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Self

from baseclasses.dataclasses.montrek_type import MontrekType, MontrekTypeEnum
from reporting.core.reporting_colors import ReportingColors

ISIN_PATTERN = re.compile(r"^[A-Z]{2}[A-Z0-9]{9}\d$")
LEI_PATTERN = re.compile(r"^[A-Z0-9]{18}\d{2}$")


def normalize_identifiers(identifiers: Iterable[str]) -> list[str]:
    """Strip, upper-case, de-duplicate and sort identifiers like ISINs or LEIs."""
    return sorted({i.strip().upper() for i in identifiers if i and i.strip()})


@dataclass(frozen=True)
class AssetType(MontrekType):
    name: str
    description: str = ""
    cfi_prefix: str = ""


class AssetTypes(MontrekTypeEnum):
    """Asset categories as defined by the first letter of the CFI code (ISO 10962)."""

    EQUITY = AssetType(
        name="EQUITY",
        color=ReportingColors.BRIGHTER_RED,
        description="Equities",
        cfi_prefix="E",
    )
    COLLECTIVE_INVESTMENT_VEHICLE = AssetType(
        name="COLLECTIVE_INVESTMENT_VEHICLE",
        color=ReportingColors.DARK_GREEN,
        description="Collective investment vehicles",
        cfi_prefix="C",
    )
    DEBT = AssetType(
        name="DEBT",
        color=ReportingColors.BLUE,
        description="Debt instruments",
        cfi_prefix="D",
    )
    ENTITLEMENT = AssetType(
        name="ENTITLEMENT",
        color=ReportingColors.PURPLE,
        description="Entitlements (rights)",
        cfi_prefix="R",
    )
    LISTED_OPTION = AssetType(
        name="LISTED_OPTION",
        color=ReportingColors.TEAL,
        description="Listed options",
        cfi_prefix="O",
    )
    FUTURE = AssetType(
        name="FUTURE",
        color=ReportingColors.BRIGHTER_ORANGE,
        description="Futures",
        cfi_prefix="F",
    )
    SWAP = AssetType(
        name="SWAP",
        color=ReportingColors.MEDIUM_BLUE,
        description="Swaps",
        cfi_prefix="S",
    )
    NON_LISTED_OPTION = AssetType(
        name="NON_LISTED_OPTION",
        color=ReportingColors.SOFT_SKY,
        description="Non-listed and complex listed options",
        cfi_prefix="H",
    )
    SPOT = AssetType(
        name="SPOT",
        color=ReportingColors.YELLOW,
        description="Spots",
        cfi_prefix="I",
    )
    FORWARD = AssetType(
        name="FORWARD",
        color=ReportingColors.DARK_ORANGE,
        description="Forwards",
        cfi_prefix="J",
    )
    STRATEGY = AssetType(
        name="STRATEGY",
        color=ReportingColors.BROWN,
        description="Strategies",
        cfi_prefix="K",
    )
    FINANCING = AssetType(
        name="FINANCING",
        color=ReportingColors.SOFT_ROSE,
        description="Financing",
        cfi_prefix="L",
    )
    REFERENTIAL_INSTRUMENT = AssetType(
        name="REFERENTIAL_INSTRUMENT",
        color=ReportingColors.DARK_BLUE,
        description="Referential instruments",
        cfi_prefix="T",
    )
    OTHER = AssetType(
        name="OTHER",
        color=ReportingColors.GREY,
        description="Others (miscellaneous)",
        cfi_prefix="M",
    )

    @classmethod
    def from_cfi_code(cls, cfi_code: str) -> Self:
        prefix = cfi_code.strip()[:1].upper()
        for member in cls:
            if member.value.cfi_prefix == prefix:
                return member
        raise ValueError(f"{cfi_code!r} is not a valid CFI code")
