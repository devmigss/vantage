import ipaddress
import socket
import time
import requests
import urllib3.util.connection as urllib3_cn

# Prefer IPv4 so requests does not stall on unreachable IPv6 addresses
urllib3_cn.allowed_gai_family = lambda: socket.AF_INET

WEATHER_CODE_MAP = {                                                                                                
    0: "Clear sky",                                                                                                 
    1: "Mainly clear",                                                                                              
    2: "Partly cloudy",                                                                                             
    3: "Overcast",                                                                                                  
    45: "Fog",                                                                                                      
    48: "Depositing rime fog",                                                                                      
    51: "Light drizzle",                                                                                            
    53: "Moderate drizzle",                                                                                         
    55: "Dense drizzle",                                                                                            
    61: "Slight rain",                                                                                              
    63: "Moderate rain",                                                                                            
    65: "Heavy rain",                                                                                               
    71: "Slight snow",                                                                                              
    73: "Moderate snow",                                                                                            
    75: "Heavy snow",                                                                                               
    80: "Slight rain showers",                                                                                      
    81: "Moderate rain showers",                                                                                    
    82: "Violent rain showers",                                                                                     
    95: "Thunderstorm",                                                                                             
}                                                                                                                   
                                                                                                                        
                                                                                                                        
def resolve_target(target=None):                                                                                    
    """                                                                                                             
    Resolves a domain name to an IPv4 address if needed.                                                            
    Returns a tuple of (resolved_ip, error_message).                                                                
    """                                                                                                             
    if not target:                                                                                                  
        return None, None                                                                                           
                                                                                                                        
    try:                                                                                                            
        ipaddress.ip_address(target)                                                                                
        return target, None                                                                                         
    except ValueError:                                                                                              
        pass                                                                                                        
                                                                                                                        
    try:                                                                                                            
        resolved_ip = socket.gethostbyname(target)                                                                  
        return resolved_ip, None                                                                                    
    except socket.gaierror:                                                                                         
        return None, f"DNS Resolution failed: could not resolve '{target}'."                                        
                                                                                                                        
                                                                                                                        
def reverse_dns_lookup(ip):                                                                                         
    """                                                                                                             
    Performs a reverse DNS (PTR) lookup for an IP address.                                                          
    Returns the hostname or 'N/A' if unavailable.                                                                   
    """                                                                                                             
    if not ip:                                                                                                      
        return "N/A"                                                                                                
    try:                                                                                                            
        hostname, _, _ = socket.gethostbyaddr(ip)                                                                   
        return hostname                                                                                             
    except (socket.herror, socket.gaierror, OSError):                                                               
        return "N/A"

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

def fetch_weather_data(lat, lon):                                                                                   
    """                                                                                                             
    Fetches current weather data for the given coordinates via Open-Meteo.                                          
    """                                                                                                             
    if lat is None or lon is None:                                                                                  
        return {"error": "Coordinates unavailable for weather lookup."}                                             
                                                                                                                        
    try:                                                                                                            
        url = "https://api.open-meteo.com/v1/forecast"                                                              
        params = {                                                                                                  
            "latitude": lat,                                                                                        
            "longitude": lon,                                                                                       
            "current_weather": "true",                                                                              
        }                                                                                                           
        response = requests.get(url, params=params, timeout=5)                                                      
                                                                                                                        
        if response.status_code != 200:                                                                             
            return {"error": f"Weather API Error: Status code {response.status_code}"}                              
                                                                                                                        
        current = response.json().get("current_weather")                                                            
        if not current:                                                                                             
            return {"error": "Weather data unavailable."}                                                           
                                                                                                                        
        code = current.get("weathercode")                                                                           
        return {                                                                                                    
            "temperature": current.get("temperature"),                                                              
            "windspeed": current.get("windspeed"),                                                                  
            "condition": WEATHER_CODE_MAP.get(code, f"Code {code}"),                                                
        }                                                                                                           
                                                                                                                        
    except requests.exceptions.ConnectionError:                                                                     
        return {"error": "Weather lookup failed: network connection error."}                                        
    except requests.exceptions.Timeout:                                                                             
        return {"error": "Weather lookup timed out."}                                                               
    except requests.exceptions.RequestException as e:                                                               
        return {"error": f"Weather lookup error: {e}"}



def measure_latency(ip, ports=(443, 80, 53), timeout=5):
    """
    Measures TCP connection latency (in ms) to the target IP across common ports.
    """
    if not ip:
        return {"error": "Target IP unavailable for latency test."}

    last_error = "Connection failed"
    for port in ports:
        try:
            start = time.perf_counter()
            with socket.create_connection((ip, port), timeout=timeout):
                elapsed_ms = (time.perf_counter() - start) * 1000
            return {
                "latency_ms": round(elapsed_ms, 2),
                "port": port,
            }
        except socket.timeout:
            last_error = "Connection timed out"
        except OSError as e:
            last_error = str(e) or "Connection refused"

    return {"error": f"Latency test failed ({last_error})."}
