import datetime
from typing import Any

from data_import.base.managers.data_import_managers import DataImportManagerABC
from data_import.base.managers.processor_base import ProcessorBaseABC
from process_pipeline.managers.pipeline_registry_manager import (
    PipelineRegistryManagerABC,
)
from data_import.base.constants import ImportStatus
from reporting.dataclasses.table_elements import (
    DateTableElement,
    StringTableElement,
)

from mt_economic_common.currency.constants import FX_SOURCE_KEY, FX_VALUE_DATE_KEY
from mt_economic_common.currency.managers.fx_rate_sources import FxRateSource
from mt_economic_common.currency.repositories.fx_rate_import_registry_repository import (
    FxRateImportRegistryRepository,
)
from mt_economic_common.currency.tasks import FxRateImportTask


class FxRateImportManager(DataImportManagerABC):
    registry_repository_class = FxRateImportRegistryRepository
    do_process_async = True
    pipeline_task_class = FxRateImportTask

    def import_fx_rates(self, source: FxRateSource, value_date: datetime.date) -> bool:
        self.set_pipeline_data(
            {
                FX_SOURCE_KEY: source.value.label,
                FX_VALUE_DATE_KEY: value_date.isoformat(),
            }
        )
        return self.trigger_pipeline()

    def additional_registry_data(self) -> dict:
        # Only known where the import is triggered; the Celery worker keeps the
        # values already stored in the registry.
        if not self.pipeline_data:
            return {}
        return {
            FX_SOURCE_KEY: self.pipeline_data[FX_SOURCE_KEY],
            FX_VALUE_DATE_KEY: datetime.date.fromisoformat(
                self.pipeline_data[FX_VALUE_DATE_KEY]
            ),
        }

    def _build_processor(self, pipeline_data: dict[str, Any]) -> ProcessorBaseABC:
        source = FxRateSource.from_label(pipeline_data[FX_SOURCE_KEY])
        return source.value.processor_class(
            self.session_data,
            pipeline_data.get("import_data", {}),
        )


class FxRateImportRegistryManager(PipelineRegistryManagerABC):
    repository_class = FxRateImportRegistryRepository
    registry_status_text_choices = ImportStatus
    status_attr = "import_status"
    message_attr = "import_message"
    status_column_name = "Import Status"
    message_column_name = "Import Message"
    date_column_name = "Imported At"
    created_by_column_name = "Imported By"

    @property
    def table_elements(self) -> tuple:
        return (
            self.date_element,
            StringTableElement(name="Source", attr=FX_SOURCE_KEY),
            DateTableElement(name="Value Date", attr=FX_VALUE_DATE_KEY),
            self.status_element,
            self.message_element,
            self.created_by_element,
        )
