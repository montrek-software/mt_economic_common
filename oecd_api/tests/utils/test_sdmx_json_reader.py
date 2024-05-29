import os
import json
from django.test import TestCase
from mt_economic_common.oecd_api.utils.sdmx_json_reader import SdmxJsonReader


class TestSdmxJsonReader(TestCase):
    def test_read_fx_annual_example(self):
        with open(
            os.path.join(
                os.path.dirname(__file__), "../test_data/fx_annual_example.json"
            )
        ) as f:
            data = json.loads(f.read())
        reader = SdmxJsonReader(json_data=data)
        result_df = reader.to_data_frame()
        self.assertEqual(result_df.shape, (16, 10))
        self.assertEqual(
            result_df.columns.tolist(),
            [
                "REF_AREA",
                "FREQ",
                "METHODOLOGY",
                "MEASURE",
                "UNIT_MEASURE",
                "EXPENDITURE",
                "ADJUSTMENT",
                "TRANSFORMATION",
                "TIME_PERIOD",
                "VALUE",
            ],
        )
        self.assertEqual(result_df["VALUE"].sum(), 1143.22449)
