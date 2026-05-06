from data_import.base.tasks.data_import_task import DataImportTask
from montrek.celery_app import SEQUENTIAL_QUEUE_NAME


class CountryRestApiUploadTask(DataImportTask):
    queue = SEQUENTIAL_QUEUE_NAME


class CountryOecdAnnualFxUploadTask(DataImportTask):
    queue = SEQUENTIAL_QUEUE_NAME


class CountryOecdInflationUploadTask(DataImportTask):
    queue = SEQUENTIAL_QUEUE_NAME
