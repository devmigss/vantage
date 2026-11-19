import sys
import os
import unittest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from cli import parse_arguments, display_result


class TestCLI(unittest.TestCase):

    @patch.object(sys, "argv", ["main.py", "-i", "8.8.8.8"])
    def test_parse_ip_argument(self):
        args = parse_arguments()
        self.assertEqual(args.ip, "8.8.8.8")

    @patch.object(sys, "argv", ["main.py"])
    def test_default_ip_argument(self):
        args = parse_arguments()
        self.assertIsNone(args.ip)

    def test_display_result(self):
        data = {
            "ip": "8.8.8.8",
            "country": "US",
            "city": "Unknown",
            "continent": "NA",
            "postal": "N/A",
            "asn": {"organization": "Google LLC"},
            "location": {
                "latitude": 37.751,
                "longitude": -97.822
            }
        }

        output = StringIO()

        with redirect_stdout(output):
            display_result(data)

        self.assertIn("8.8.8.8", output.getvalue())
        self.assertIn("Google LLC", output.getvalue())


if __name__ == "__main__":
    unittest.main()
