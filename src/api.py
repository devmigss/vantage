import requests

def fetch_network_data(ip=None):
    try:
        # 1. Format the URL based on whether an IP was provided
        if ip:
            url = f"https://api.country.is/{ip}?fields=city,continent,subdivision,postal,location,asn"
        else:
            url = "https://api.country.is/?fields=city,continent,subdivision,postal,location,asn"

        # 2. Make the request
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: Status code {response.status_code}"}

    except requests.exceptions.ConnectionError:
        return {"error": "Network connection failed. Please check your internet."}
    except requests.exceptions.Timeout:
        return {"error": "Connection timed out. The network is too slow."}
    except requests.exceptions.RequestException as e:
        return {"error": f"An unexpected error occurred: {e}"}