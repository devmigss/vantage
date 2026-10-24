import requests

def fetch_network_data():
    try:
        response = requests.get('https://api.country.is/?fields=city,continent,subdivision,postal,location,asn', timeout=5)

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
