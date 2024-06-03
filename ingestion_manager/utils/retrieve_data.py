import time
import requests
from .setup import config, URLS

def check_api_key() -> bool:
    """
    Checks if the API key is set.

    Returns:
        bool: True if API key is set, False otherwise.
    """
    return config['API_KEY'] is not None


def is_valid_response(response: dict) -> bool:
    """
    Checks if the response is valid.
    Parameters:
        response (dict): The response to be checked.
    Returns:
        bool: True if the response is valid, False otherwise.
    """
    return response.get("status") == "success"


def make_request(url: str) -> dict:
    """
    Makes a request to the given URL and handles retries if the response is invalid.
    Args:
        url (str): The URL to make the request to.
    Returns:
        dict: The response data as a dictionary.
    """
    response = requests.get(url, timeout=15).json()
    while not is_valid_response(response):
        error = response.get("data", {}).get("message", "Unknown error")
        if error == "state_not_found":
            print(f"[ingestion_manager] Failed to fetch data. {error}")
            return {}
        print(f"[ingestion_manager] Failed to fetch data. {error}. Waiting 5 sec. [CTRL+C to stop]")
        time.sleep(5)
        response = requests.get(url, timeout=15).json()
    return response.get("data", {})


def get_data() -> dict:
    """
    Handles the retrieval of air quality data based on the specified action.
    Returns:
        dict: The retrieved air quality data.
    """
    action = config['DATA_ACTION']
    url = URLS.get(action)
    if url:
        return make_request(url)
    return {}



def get_all_countries() -> list:
    """
    Retrieves all countries.
    Returns:
        list: A list of all countries.
    """
    return make_request(URLS["ALL_COUNTRIES"])


def get_states_by_country(country_name: str) -> dict:
    """
    Retrieves all states for a given country.
    Args:
        country_name (str): The name of the country.
    Returns:
        dict: A dict of states for the given country.
    """
    url = f"http://api.airvisual.com/v2/states?country={country_name}&key={config['API_KEY']}"
    return make_request(url)


def get_cities_by_state_country(state_name: str, country_name: str) -> dict:
    """
    Retrieves cities for a given state and country.
    Args:
        state_name (str): The name of the state.
        country_name (str): The name of the country.
    Returns:
        dict: A dict of cities for the given state and country.
    """
    url = f"http://api.airvisual.com/v2/cities?state={state_name}&country=\
            {country_name}&key={config['API_KEY']}"
    return make_request(url)
