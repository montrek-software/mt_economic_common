from django.test import SimpleTestCase

from mt_economic_common.market_data.utils import AssetTypes


class TestAssetTypes(SimpleTestCase):
    def test_from_cfi_code(self):
        self.assertEqual(AssetTypes.from_cfi_code("ESVUFR"), AssetTypes.EQUITY)
        self.assertEqual(AssetTypes.from_cfi_code(" dbftfb"), AssetTypes.DEBT)
        self.assertEqual(
            AssetTypes.from_cfi_code("CIOGEU"), AssetTypes.COLLECTIVE_INVESTMENT_VEHICLE
        )

    def test_from_cfi_code_invalid(self):
        for code in ("", "ZXXXXX"):
            with self.assertRaises(ValueError):
                AssetTypes.from_cfi_code(code)

    def test_cfi_prefixes_are_unique(self):
        prefixes = [member.value.cfi_prefix for member in AssetTypes]
        self.assertEqual(len(prefixes), len(set(prefixes)))
