import requests
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
from .setup import config


def check_api_key() -> bool:
    """
    Checks if the API key is set.

    Returns:
        bool: `True` if API key is set, `False` otherwise.
    """
    return config['API_KEY'] is not None



async def make_request(url: str) -> dict:
    """
    Makes a request to the given URL and handles retries if the response is invalid.
    Args:
        url (`str`): The URL to make the request to.
    Returns:
        `dict`: The response data as a dictionary.
    """
    response = requests.get(url, timeout=15).json()
    return response


def load_city_coordinates(file_path) -> dict:
    """
    Load city coordinates from a JSON file.

    Args:
        file_path (`str`): The path to the JSON file.

    Returns:
        `dict`: A dictionary containing the city coordinates.

    Raises:
        `FileNotFoundError`: If the specified file does not exist.

    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_city_coordinates(file_path, city_coordinates) -> None:
    """
    Save the city coordinates to a JSON file.

    Args:
        file_path (str): The path to the JSON file.
        city_coordinates (dict): A dictionary containing the city coordinates.

    Returns:
        None
    """
    with open(file_path, 'w') as f:
        json.dump(city_coordinates, f, indent=4)


async def get_coord(city: str) -> dict:
    """
    Gets the coordinates of a city.

    Args:
        city (str): The name of the city.

    Returns:
        dict: The coordinates of the city.

    Raises:
        GeopyError: If an error occurs while fetching the location.
        Exception: If an unexpected error occurs.

    Notes:
        This function uses the `Nominatim` geocoder from the `geopy` library to retrieve the coordinates of a city.
        If the city is found in the `city_coord` dictionary, the coordinates are returned directly.
        If the city is not found, the geocoder is used to fetch the location.
        If the location is found, the coordinates are saved in the `city_coord` dictionary and returned.
        If the location is not found, an error message is returned.
        If an error occurs during the process, an error message is returned.

    Example:
        >>> get_coord("London")
        {'lat': 51.5073219, 'lon': -0.1276474}
    """
    city_coord = load_city_coordinates("./data/city_coord.json")
    if city in city_coord:
        return {'lat': city_coord[city][0], 'lon': city_coord[city][1]}

    geolocator = Nominatim(user_agent="aqm")
    try:
        location = geolocator.geocode(city)
        if location:
            city_coord[city] = [location.latitude, location.longitude]
            save_city_coordinates("./data/city_coord.json", city_coord)
            return {'lat': location.latitude, 'lon': location.longitude}
        else:
            return {'error': f'Location "{city}" not found'}
    except (GeopyError, Exception) as e:
        return {'error': f'Error occurred while fetching the location for "{city}": {str(e)}'}
