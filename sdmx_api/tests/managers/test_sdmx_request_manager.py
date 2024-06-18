import sdmx
from django.test import TestCase
from mt_economic_common.sdmx_api.managers.sdmx_request_manager import SdmxRequestManager
from unittest.mock import patch, MagicMock


class TestSdmxRequestManager(TestCase):
    @patch("sdmx.read_url")
    @patch("api_upload.managers.request_manager.RequestManagerABC.get_endpoint_url")
    def test_get_sdmx_request(self, mock_get_endpoint_url, mock_read_url):
        # Arrange
        test_request_manager = SdmxRequestManager()

        # Creating a mock DataMessage with necessary attributes and methods
        fake_data_message = MagicMock(spec=sdmx.message.DataMessage)
        fake_data_message.data = [MagicMock()]
        fake_data_message.data[0].series = [MagicMock()]

        mock_read_url.return_value = fake_data_message
        mock_get_endpoint_url.return_value = "http://example.com/TEST"

        # Mock sdmx.to_pandas to return a fake pandas DataFrame or dict
        expected_data = {"data": "fake_data"}
        with patch("sdmx.to_pandas", return_value=expected_data):
            # Act
            response = test_request_manager.get_response("TEST")

            # Assert
            mock_get_endpoint_url.assert_called_once_with("TEST")
            mock_read_url.assert_called_once_with("http://example.com/TEST")
            self.assertEqual(response, expected_data)

    def test_failings_get_sdmx_request(self):
        # Arrange
        test_request_manager = SdmxRequestManager()
        with patch("sdmx.read_url", side_effect=Exception("Test error")):
            # Act
            response = test_request_manager.get_response("TEST")
            # Assert
            self.assertTrue(response.empty)
            self.assertEqual(
                test_request_manager.message,
                "Error raised during object creation: Exception: Test error",
            )
