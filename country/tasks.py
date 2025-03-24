from api_upload.tasks import ApiUploadTask
from data_import.base.tasks.data_import_task import DataImportTask
from montrek.celery_app import SEQUENTIAL_QUEUE_NAME

from mt_economic_common.country.managers.country_manager import (
    RestCountriesUploadManager,
)
from mt_economic_common.country.managers.country_oecd_manager import (
    CountryOecdAnnualFxUploadManager,
    CountryOecdInflationUploadManager,
)


class CountryRestApiUploadTask(DataImportTask):
    manager_class = RestCountriesUploadManager
    queue=SEQUENTIAL_QUEUE_NAME

country_rest_api_upload_task = CountryRestApiUploadTask()


class CountryOecdAnnualFxUploadTask(ApiUploadTask):
    api_upload_manager_class = CountryOecdAnnualFxUploadManager


country_oecd_annual_fx_upload_task = CountryOecdAnnualFxUploadTask(
    queue=SEQUENTIAL_QUEUE_NAME
)


class CountryOecdInflationUploadTask(ApiUploadTask):
    api_upload_manager_class = CountryOecdInflationUploadManager


country_oecd_infation_upload_task = CountryOecdInflationUploadTask(
    queue=SEQUENTIAL_QUEUE_NAME
)
