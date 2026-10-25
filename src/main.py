import sys
from cli import parse_arguments, display_result, display_error
from api import fetch_network_data

def main():
    print("🚦 1. Starting Vantage...")

    args = parse_arguments()
    print(f"✅ 2. Arguments parsed. Target IP: {args.ip}")

    try:
        print("🌐 3. Fetching data from API... (This might take a second)")
        data = fetch_network_data(args.ip)

        print("📊 4. Data received, sending to display...")
        display_result(data)

    except Exception as e:
        display_error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()