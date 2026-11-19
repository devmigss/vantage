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

    def test_display_result_with_dns_and_weather(self):                                                                                 
        data = {                                                                                                                        
            "ip": "8.8.8.8",                                                                                                            
            "country": "US",                                                                                                            
            "city": "Mountain View",                                                                                                    
            "continent": "NA",                                                                                                          
            "postal": "94043",                                                                                                          
            "asn": {"organization": "Google LLC"},                                                                                      
            "location": {"latitude": 37.386, "longitude": -122.0838},                                                                   
        }                                                                                                                               
        weather = {                                                                                                                     
            "temperature": 21.0,                                                                                                        
            "windspeed": 8.5,                                                                                                           
            "condition": "Clear sky",                                                                                                   
        }                                                                                                                               
                                                                                                                                            
        output = StringIO()                                                                                                             
        with redirect_stdout(output):                                                                                                   
            display_result(data, dns_hostname="dns.google", weather=weather)                                                            
                                                                                                                                            
        result = output.getvalue()                                                                                                      
        self.assertIn("dns.google", result)                                                                                             
        self.assertIn("21.0°C, Clear sky", result)


if __name__ == "__main__":
    unittest.main()
