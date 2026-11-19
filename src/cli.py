import argparse
import sys


def parse_arguments():
    """
    Parses command-line arguments for the Vantage application.
    Returns the parsed arguments object.
    """
    parser = argparse.ArgumentParser(
        prog="vantage",
        description="Vantage: Instant network data retrieval, DNS resolution, and weather."
    )

    parser.add_argument(
        "-i", "--ip",
        type=str,
        help="Target IP address or domain name to inspect. Leave blank to check your own network.",
        default=None
    )

    return parser.parse_args()


def display_result(
    data: dict,
    dns_hostname: str = None,
    weather: dict = None,
    latency: dict = None,
):
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

    hostname_display = dns_hostname or "N/A"

    if weather and "error" not in weather:
        temp = weather.get("temperature", "N/A")
        wind = weather.get("windspeed", "N/A")
        condition = weather.get("condition", "Unknown")
        weather_display = f"{temp}°C, {condition} (Wind: {wind} km/h)"
    elif weather and "error" in weather:
        weather_display = f"Unavailable ({weather['error']})"
    else:
        weather_display = "N/A"

    if latency and "error" not in latency:
        latency_display = f"{latency.get('latency_ms', 'N/A')} ms (TCP/{latency.get('port', 'N/A')})"
    elif latency and "error" in latency:
        latency_display = f"Unavailable ({latency['error']})"
    else:
        latency_display = "N/A"

    print("\n" + "=" * 45)
    print(" 🌍  VANTAGE NETWORK INTELLIGENCE")
    print("=" * 45)
    print(f" 📡 IP Address  : {ip}")
    print(f" 🌐 Hostname    : {hostname_display}")
    print(f" 🗺️  Location    : {city}, {country} ({continent})")
    print(f" 📮 Postal Code : {postal}")
    print(f" 📍 Coordinates : {lat}, {lon}")
    print(f" 🏢 ISP Provider: {asn_name}")
    print(f" 🌤️  Weather     : {weather_display}")
    print(f" ⚡ Latency     : {latency_display}")
    print("=" * 45 + "\n")


def display_error(error_message: str):
    print("\n❌ Vantage Error ❌")
    print(f"{error_message}\n", file=sys.stderr)
