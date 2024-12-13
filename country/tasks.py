from api_upload.tasks import ApiUploadTask
from montrek.celery_app import app as celery_app

from mt_economic_common.country.managers.country_manager import (
    RestCountriesUploadManager,
)
from mt_economic_common.country.managers.country_oecd_manager import (
    CountryOecdAnnualFxUploadManager,
    CountryOecdInflationUploadManager,
)


class CountryRestApiUploadTask(ApiUploadTask):
    api_upload_manager_class = RestCountriesUploadManager


class CountryOecdAnnualFxUploadTask(ApiUploadTask):
    api_upload_manager_class = CountryOecdAnnualFxUploadManager


class CountryOecdInflationUploadTask(ApiUploadTask):
    api_upload_manager_class = CountryOecdInflationUploadManager
