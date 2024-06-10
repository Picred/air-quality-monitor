import requests
from geopy.geocoders import Nominatim
from .setup import config

def check_api_key() -> bool:
    """
    Checks if the API key is set.

    Returns:
        bool: `True` if API key is set, `False` otherwise.
    """
    return config['API_KEY'] is not None


def is_valid_response(response: dict) -> bool:
    """
    Checks if the response is valid.
    Parameters:
        response (`dict`): The response to be checked.
    Returns:
        `bool`: True if the response is valid, False otherwise.
    """
    return response.get("status") == "success"


def make_request(url: str) -> dict:
    """
    Makes a request to the given URL and handles retries if the response is invalid.
    Args:
        url (`str`): The URL to make the request to.
    Returns:
        `dict`: The response data as a dictionary.
    """
    response = requests.get(url, timeout=15).json()
    return response


def get_coord(city: str) -> dict:
    """
    Gets the coordinates of a city.

    Args:
        city (`str`): The name of the city.

    Returns:
        `dict`: The coordinates of the city.
    """
    geolocator = Nominatim(user_agent="aqm")

    location = geolocator.geocode(city)
    if location:
        return {'lat': location.latitude, 'lon': location.longitude}
    else:
        return {'error': f'Location \"{city}\" not found'}
