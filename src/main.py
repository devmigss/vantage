import sys
from cli import parse_arguments, display_result, display_error
from api import (
    resolve_target,
    reverse_dns_lookup,
    fetch_network_data,
    fetch_weather_data,
    measure_latency,
)


def main():
    print("🚦 1. Starting Vantage...")

    args = parse_arguments()
    print(f"✅ 2. Arguments parsed. Target: {args.ip}")

    try:
        resolved_ip, dns_error = resolve_target(args.ip)
        if dns_error:
            display_error(dns_error)
            sys.exit(1)

        if args.ip and resolved_ip != args.ip:
            print(f"🔎 2b. Resolved '{args.ip}' -> {resolved_ip}")

        print("🌐 3. Fetching network data from API... (This might take a second)")
        data = fetch_network_data(resolved_ip)

        if "error" in data:
            display_result(data)
            return

        print("🧭 4. Performing reverse DNS lookup...")
        hostname = reverse_dns_lookup(data.get("ip"))

        print("🌤️  5. Fetching weather data...")
        location = data.get("location") or {}
        weather = fetch_weather_data(
            location.get("latitude"),
            location.get("longitude"),
        )

        print("⚡ 6. Measuring network latency...")
        latency = measure_latency(data.get("ip"))

        print("📊 7. Data received, sending to display...")
        display_result(
            data,
            dns_hostname=hostname,
            weather=weather,
            latency=latency,
        )

    except Exception as e:
        display_error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
