import sys
import os
import unittest
from unittest.mock import patch, Mock

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from api import fetch_network_data


class TestFetchNetworkData(unittest.TestCase):

    @patch("api.requests.get")
    def test_successful_request(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"city": "Test City"}
        mock_get.return_value = mock_response

        result = fetch_network_data("8.8.8.8")

        self.assertEqual(result["city"], "Test City")

    @patch("api.requests.get")
    def test_api_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = fetch_network_data("8.8.8.8")

        self.assertEqual(result["error"], "API Error: Status code 500")

    @patch("api.requests.get")
    def test_connection_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError

        result = fetch_network_data("8.8.8.8")

        self.assertIn("Network connection failed", result["error"])

    @patch("api.requests.get")
    def test_timeout_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.exceptions.Timeout

        result = fetch_network_data("8.8.8.8")

        self.assertIn("Connection timed out", result["error"])


if __name__ == "__main__":
    unittest.main()
