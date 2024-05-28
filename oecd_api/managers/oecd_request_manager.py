import pandas as pd
from api_upload.managers.request_manager import RequestManager
from mt_economic_common.oecd_api.utils.sdmx_json_reader import SdmxJsonReader
from mt_economic_common.country.repositories.country_repository import CountryRepository


class OecdRequestManager(RequestManager):
    base_url = "https://sdmx.oecd.org/public/rest/data/"

    def get_endpoint_url(self, endpoint: str) -> str:
        return super().get_endpoint_url(endpoint) + "&format=jsondata"

    def get_average_annual_fx_rates(self) -> pd.DataFrame:
        test_json = self.get_json(
            "OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE4,1.0/A....EXC_A.......?startPeriod=2000"
        )
        reader = SdmxJsonReader(json_data=test_json, dimension_out="id")
        result_df = reader.to_data_frame()
        result_df = self._map_to_currency_code(result_df)
        return result_df

    def _map_to_currency_code(self, df: pd.DataFrame) -> pd.DataFrame:
        country_queryset = CountryRepository().std_queryset()
        country_queryset = country_queryset.filter(
            country_name__in=df["REF_AREA"].unique()
        )
        country_currency_map = {c.country_code: c.ccy_code for c in country_queryset}
        df["CCY_CODE"] = df["REF_AREA"].map(country_currency_map)
        return df
