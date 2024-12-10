from api_upload.tasks import ApiUploadTask
from montrek.celery_app import app as celery_app

from mt_economic_common.country.managers.country_manager import (
    RestCountriesUploadManager,
)


class CountryRestApiUploadTask(ApiUploadTask):
    api_upload_manager_class = RestCountriesUploadManager


COUNTRY_REST_API_UPLOAD_TASK = CountryRestApiUploadTask()
celery_app.register_task(COUNTRY_REST_API_UPLOAD_TASK)
