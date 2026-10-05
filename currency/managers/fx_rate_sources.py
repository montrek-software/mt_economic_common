from dataclasses import dataclass

from baseclasses.utils import ChoicesEnum

from mt_economic_common.currency.managers.fx_rate_import_processors import (
    DummyFxRateImportProcessor,
    FrankfurterFxRateImportProcessor,
    FxRateImportProcessorABC,
)


@dataclass(frozen=True)
class FxRateSourceDataClass:
    label: str
    description: str
    processor_class: type[FxRateImportProcessorABC]


class FxRateSource(ChoicesEnum):
    """The sources FX rates can be imported from.

    The label is stored in the import registry, so it must stay stable once used.
    """

    DUMMY = FxRateSourceDataClass(
        label="dummy",
        description="Dummy (every FX rate set to 1)",
        processor_class=DummyFxRateImportProcessor,
    )
    FRANKFURTER = FxRateSourceDataClass(
        label="frankfurter",
        description="Frankfurter (ECB reference rates)",
        processor_class=FrankfurterFxRateImportProcessor,
    )

    @classmethod
    def to_list(cls) -> list[tuple[str, str]]:
        return [(member.value.label, member.value.description) for member in cls]

    @classmethod
    def from_label(cls, label: str) -> "FxRateSource":
        for member in cls:
            if member.value.label == label:
                return member
        raise KeyError(f"Unknown FX rate source '{label}'")
