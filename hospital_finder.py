# hospital_finder.py
import webbrowser
import requests

IPINFO_URL = "https://ipinfo.io/json"

def open_hospitals_near(location: str) -> str:
    """
    Opens Google Maps in browser showing hospitals near the given location.
    Returns a status message for the chat window.
    """
    query = f"hospitals near {location}"
    url = "https://www.google.com/maps/search/" + query.replace(" ", "+")
    webbrowser.open(url)
    return f"Opening hospitals near <b>{location}</b> in your browser..."

def auto_detect_and_open() -> str:
    """
    Uses IP-based geolocation to approximate user's city.
    Then opens hospitals near that city on Google Maps.
    """
    try:
        resp = requests.get(IPINFO_URL, timeout=5)
        if resp.status_code != 200:
            return "Sorry, I could not detect your location automatically. Please try manual city/pincode."

        data = resp.json()
        city = data.get("city", "")
        region = data.get("region", "")
        country = data.get("country", "")

        if not city and not region:
            return "Sorry, automatic location info is incomplete. Please try manual city/pincode."

        location_str = ", ".join([p for p in [city, region, country] if p])
        return open_hospitals_near(location_str)

    except Exception as e:
        return f"Automatic location failed ({e}). Please enter your city or pincode manually."
