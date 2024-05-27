from django.test import TestCase
from mt_economic_common.oecd_api.managers.oecd_request_manager import OecdRequestManager
from mt_economic_common.oecd_api.utils.sdmx_json_reader import SdmxJsonReader


class TestOecdRequestManager(TestCase):
    def test_get_endpoint_url(self):
        manager = OecdRequestManager()
        endpoint = "test_endpoint"
        expected_url = (
            "https://sdmx.oecd.org/public/rest/data/test_endpoint&format=jsondata"
        )
        self.assertEqual(manager.get_endpoint_url(endpoint), expected_url)

    def test_get_fx_annual(self):
        manager = OecdRequestManager()
        test_json = manager.get_json(
            "OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE4,1.0/A....EXC_A.......?startPeriod=2000"
        )
        reader = SdmxJsonReader(json_data=test_json)
        result_df = reader.to_data_frame()
        breakpoint()
