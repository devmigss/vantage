import sys
import os
import unittest
from unittest.mock import patch, Mock

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from api import (
    fetch_network_data,
    resolve_target,
    reverse_dns_lookup,
    fetch_weather_data,
    measure_latency,
)


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


class TestDNSResolution(unittest.TestCase):

    def test_resolve_valid_ip_returns_unchanged(self):
        ip, error = resolve_target("8.8.8.8")
        self.assertEqual(ip, "8.8.8.8")
        self.assertIsNone(error)

    @patch("api.socket.gethostbyname", return_value="142.250.190.78")
    def test_resolve_domain_success(self, mock_resolve):
        ip, error = resolve_target("google.com")
        self.assertEqual(ip, "142.250.190.78")
        self.assertIsNone(error)

    @patch("api.socket.gethostbyname")
    def test_resolve_domain_failure(self, mock_resolve):
        import socket
        mock_resolve.side_effect = socket.gaierror
        ip, error = resolve_target("invalid.domain.test")
        self.assertIsNone(ip)
        self.assertIn("DNS Resolution failed", error)

    @patch("api.socket.gethostbyaddr", return_value=("dns.google", [], ["8.8.8.8"]))
    def test_reverse_dns_success(self, mock_rdns):
        self.assertEqual(reverse_dns_lookup("8.8.8.8"), "dns.google")

    @patch("api.socket.gethostbyaddr")
    def test_reverse_dns_fallback(self, mock_rdns):
        import socket
        mock_rdns.side_effect = socket.herror
        self.assertEqual(reverse_dns_lookup("8.8.8.8"), "N/A")


class TestFetchWeatherData(unittest.TestCase):

    @patch("api.requests.get")
    def test_weather_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "current_weather": {
                "temperature": 22.5,
                "windspeed": 10.2,
                "weathercode": 0,
            }
        }
        mock_get.return_value = mock_response

        result = fetch_weather_data(37.751, -97.822)
        self.assertEqual(result["temperature"], 22.5)
        self.assertEqual(result["condition"], "Clear sky")

    @patch("api.requests.get")
    def test_weather_api_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 503
        mock_get.return_value = mock_response

        result = fetch_weather_data(37.751, -97.822)
        self.assertIn("Weather API Error", result["error"])


class TestMeasureLatency(unittest.TestCase):

    def test_measure_latency_missing_ip(self):
        result = measure_latency(None)
        self.assertIn("Target IP unavailable", result["error"])

    @patch("api.time.perf_counter", side_effect=[1.000, 1.025])
    @patch("api.socket.create_connection")
    def test_measure_latency_success(self, mock_conn, mock_timer):
        mock_conn.return_value.__enter__ = Mock()
        mock_conn.return_value.__exit__ = Mock(return_value=False)

        result = measure_latency("8.8.8.8")
        self.assertEqual(result["latency_ms"], 25.0)
        self.assertEqual(result["port"], 443)

    @patch("api.time.perf_counter", side_effect=[1.000, 2.000, 2.012])
    @patch("api.socket.create_connection")
    def test_measure_latency_fallback_port(self, mock_conn, mock_timer):
        mock_ctx = Mock()
        mock_ctx.__enter__ = Mock()
        mock_ctx.__exit__ = Mock(return_value=False)
        mock_conn.side_effect = [OSError("Connection refused"), mock_ctx]

        result = measure_latency("8.8.8.8", ports=(443, 80))
        self.assertEqual(result["latency_ms"], 12.0)
        self.assertEqual(result["port"], 80)

    @patch("api.socket.create_connection")
    def test_measure_latency_timeout(self, mock_conn):
        import socket
        mock_conn.side_effect = socket.timeout

        result = measure_latency("8.8.8.8", ports=(443,))
        self.assertIn("Connection timed out", result["error"])


if __name__ == "__main__":
    unittest.main()
