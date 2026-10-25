import argparse
import sys

def parse_arguments():
    """
    Parses command-line arguments for the Vantage application.
    Returns the parsed arguments object.
    """
    parser = argparse.ArgumentParser(
        prog="vantage",
        description="Vantage: Instant network data retrieval and geolocation."
    )

    parser.add_argument(
        "-i", "--ip",
        type=str,
        help="Target IP address to inspect. Leave blank to check your own network.",
        default=None
    )

    return parser.parse_args()


def display_result(data: dict):
    if "error" in data:
        display_error(data["error"])
        return

    ip = data.get("ip") or "Unknown"
    country = data.get("country") or "Unknown"
    city = data.get("city") or "Unknown"
    continent = data.get("continent") or "Unknown"
    postal = data.get("postal") or "N/A"

    asn = data.get("asn", {})
    asn_name = asn.get("organization") or "Unknown"

    location = data.get("location", {})
    lat = location.get("latitude", "N/A")
    lon = location.get("longitude", "N/A")

    print("\n" + "=" * 45)
    print(" 🌍  VANTAGE NETWORK INTELLIGENCE")
    print("=" * 45)
    print(f" 📡 IP Address  : {ip}")
    print(f" 🗺️  Location    : {city}, {country} ({continent})")
    print(f" 📮 Postal Code : {postal}")
    print(f" 📍 Coordinates : {lat}, {lon}")
    print(f" 🏢 ISP Provider    : {asn_name}")
    print("=" * 45 + "\n")

def display_error(error_message: str):
    print("\n❌ Vantage Error ❌")
    print(f"{error_message}\n", file=sys.stderr)