from api_upload.tasks import ApiUploadTask

from mt_economic_common.country.managers.country_manager import (
    RestCountriesUploadManager,
)
from mt_economic_common.country.managers.country_oecd_manager import (
    CountryOecdAnnualFxUploadManager,
    CountryOecdInflationUploadManager,
)


class CountryRestApiUploadTask(ApiUploadTask):
    api_upload_manager_class = RestCountriesUploadManager


country_rest_api_upload_task = CountryRestApiUploadTask()


class CountryOecdAnnualFxUploadTask(ApiUploadTask):
    api_upload_manager_class = CountryOecdAnnualFxUploadManager


country_oecd_annual_fx_upload_task = CountryOecdAnnualFxUploadTask()


class CountryOecdInflationUploadTask(ApiUploadTask):
    api_upload_manager_class = CountryOecdInflationUploadManager


country_oecd_infation_upload_task = CountryOecdInflationUploadTask()
