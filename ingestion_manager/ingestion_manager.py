"""Handles the data ingestion process for air quality.

This module contains functions to retrieve air quality data from the AirVisual API,
send data to Logstash for ingestion, and parse raw data to extract relevant weather
and air quality information.

Environment Variables:
    API_KEY (str): The API key for accessing AirVisual data.
    COUNTRY_NAME (str): The name of the country of interest to retrieve data for.
    STATE_NAME (str): The name of the state within the country.
    GPS_LAT (float): The latitude for GPS location identification for data retrieval.
    GPS_LON (float): The longitude for GPS location identification for data retrieval.
    CITY_TO_SCAN (str): The name of the city of interest for data retrieval.
    DATA_ACTION (str): The action to perform for data retrieval (e.g., "NEAREST_IP_CITY").

Functions:
    get_data: Retrieves air quality data based on the specified action.
    send_to_logstash: Sends data to Logstash for ingestion.
    extract_data: Extracts relevant air quality data from the raw JSON response.
    test_logstash: Checks if Logstash is ready to receive data.
    check_api_key: Checks if the API key is set.
    main: The main asynchronous function for executing the script.
"""
import asyncio
import json
import sys
import time
import socket
import os
import requests
from pylogbeat import PyLogBeatClient

API_KEY = os.getenv("API_KEY", "0e72cb61-87b6-4ab4-b422-0886e1305ac6")
COUNTRY_NAME = os.getenv("COUNTRY_NAME", "Italy")
STATE_NAME = os.getenv("STATE_NAME", "Sicily")
GPS_LAT = float(os.getenv("GPS_LAT", "37.500000"))
GPS_LON = float(os.getenv("GPS_LON", "15.090278"))
CITY_TO_SCAN = os.getenv("CITY_TO_SCAN", "Catania")
DATA_ACTION = os.getenv("DATA_ACTION", "ALL_CITIES_BY_STATE_COUNTRY")

ALL_COUNTRIES_URL = f"http://api.airvisual.com/v2/countries?key={API_KEY}"
ALL_STATES_BY_COUNTRY_URL = f"http://api.airvisual.com/v2/states?country={COUNTRY_NAME}&key={API_KEY}"
ALL_CITIES_BY_STATE_COUNTRY_URL = f"http://api.airvisual.com/v2/cities?state={STATE_NAME}&country={COUNTRY_NAME}&key={API_KEY}"

NEAREST_IP_CITY_URL = f"http://api.airvisual.com/v2/nearest_city?key={API_KEY}"
NEAREST_GPS_CITY_URL = f"http://api.airvisual.com/v2/nearest_city?lat={GPS_LAT}&lon={GPS_LON}&key={API_KEY}"
SPECIFIC_CITY_URL = f"http://api.airvisual.com/v2/city?city={CITY_TO_SCAN}&state={STATE_NAME}&country={COUNTRY_NAME}&key={API_KEY}"

LOGSTASH_PORT = 5044
LOGSTASH_HOSTNAME = "logstash"

def get_data() -> dict:
    """
    Handles the retrieval of air quality data based on the specified action.

    Returns:
        dict: The json response containing air quality data.
    """
    match DATA_ACTION:
        case "ALL_COUNTRIES":
            return requests.get(f"{ALL_COUNTRIES_URL}", timeout=15).json()
        case "ALL_STATES_BY_COUNTRY":
            return requests.get(f"{ALL_STATES_BY_COUNTRY_URL}", timeout=15).json()
        case "ALL_CITIES_BY_STATE_COUNTRY":
            return requests.get(f"{ALL_CITIES_BY_STATE_COUNTRY_URL}", timeout=15).json()
        case "NEAREST_IP_CITY":
            return requests.get(f"{NEAREST_IP_CITY_URL}", timeout=15).json()
        case "NEAREST_GPS_CITY":
            return requests.get(f"{NEAREST_GPS_CITY_URL}", timeout=15).json()
        case "SPECIFIC_CITY":
            return requests.get(f"{SPECIFIC_CITY_URL}", timeout=15).json()


def get_data_handler() -> dict:
    """
    Retrieves air quality data based on the specified action.

    Returns:
        dict: The json response containing air quality data.
    """
    response = get_data()

    while not is_valid_response(response):
        error = response.get("data", []).get("message", "Unknown error")
        print(f"[ingestion_manager] Failed to fetch data. {error}. Waiting 5 sec.. [CTRL+C to stop]")
        time.sleep(5)
        response = get_data()
    return response


def check_api_key() -> bool:
    """
    Checks if the API key is set.

    Returns:
        bool: True if API key is set, False otherwise.
    """
    return API_KEY is not None


def test_logstash() -> None:
    """
    Checks if Logstash is ready for receiving data.
    """
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((LOGSTASH_HOSTNAME, LOGSTASH_PORT))
            sock.close()
            print("[ingestion_manager] Logstash is ready!")
            break
        except socket.error:
            print("[ingestion_manager] Logstash not ready, waiting... [CTRL+C to stop]")
            time.sleep(5)
            continue


def send_to_logstash(host: str, port: int, data: dict) -> None:
    """
    Sends data to Logstash for ingestion.

    Args:
        host (str): The hostname or IP address of the Logstash server.
        port (int): The port number of the Logstash server.
        data (dict): The data to be sent to Logstash.
    """
    if type(data.get("data")) == list:
        print(data)
        return
    client = PyLogBeatClient(host, port)
    client.send([json.dumps(data)])
    print("[ingestion_manager] Sent to Logstash! 🚀")

def is_valid_response(response: dict) -> bool:
    """
    Checks if the response is valid.

    Args:
        response (dict): The response to check.

    Returns:
        bool: True if the response is valid, False otherwise.
    """
    return response.get("status") == "success"

def get_all_countries() -> list:
    """
    Retrieves all countries.
    """
    response = requests.get(ALL_COUNTRIES_URL, timeout=15).json()
    
    while not is_valid_response(response):
        error = response.get("data", []).get("message", "Unknown error")
        print(f"[ingestion_manager] Failed to fetch data. {error}. Waiting 5 sec.. [CTRL+C to stop]")
        time.sleep(5)
        response = requests.get(ALL_COUNTRIES_URL, timeout=15).json()

    countries = response.get("data", [])
    return countries

def get_states_by_country(country_name: str) -> list:
    """
    Retrieves all states for a given country.
    """
    url = f"http://api.airvisual.com/v2/states?country={country_name}&key={API_KEY}"
    response = requests.get(url, timeout=15).json()

    while not is_valid_response(response):
        error = response.get("data", []).get("message", "Unknown error")
        print(f"[ingestion_manager] Failed to fetch data. {error}. Waiting 5 sec.. [CTRL+C to stop]")
        time.sleep(5)
        response = requests.get(url, timeout=15).json()

    states = response.get("data", [])
    return states

def get_cities_by_state_country(state_name: str, country_name: str) -> list:
    """
    Retrieves cities for a given state and country.
    """
    url = f"http://api.airvisual.com/v2/cities?state={state_name}&country={country_name}&key={API_KEY}"
    response = requests.get(url, timeout=15).json()

    while not is_valid_response(response):
        error = response.get("data", []).get("message", "Unknown error")
        print(f"[ingestion_manager] Failed to fetch data. {error}. Waiting 5 sec.. [CTRL+C to stop]")
        time.sleep(5)
        response = requests.get(url, timeout=15).json()
    
    cities = response.get("data", [])
    return cities


async def main() -> None:
    """
    The main asynchronous function for executing the script.
    """
    print("[ingestion_manager] Starting data ingestion process...")
    print("[ingestion_manager] This is not a demo. Real data will be retrieved. It may take a while. 🕒")
    print(f"[ingestion_manager] Selected country: {COUNTRY_NAME}")
    print("[ingestion_manager] Retrieving data of major of cities...")
    states = get_states_by_country(COUNTRY_NAME)
    states_list = [elem['state'] for elem in states]

    states_list.remove("Abruzzo") # Abruzzo is not in the list of allowed states
    states_list.remove("Basilicate") # Basilicate is not in the list of allowed states

    time.sleep(1)

    for state in states_list:
        state = state.replace(" ", "+")
        print(f"State retrieved: {state}")
        cities = get_cities_by_state_country(state, COUNTRY_NAME)

        city_present = any('city' in elem for elem in cities)
        if not city_present:
            print("[ingestion_manager] No cities found for this state. Maybe too many requests. Waiting 10 sec.. [CTRL+C to stop]")
            time.sleep(10)
            continue

        cities_list = [elem['city'] for elem in cities if 'city' in elem]
        print(f"[ingestion_manager] Retrieved cities {cities_list}")
        time.sleep(10)

        city = cities_list[0]
        city = city.replace(" ", "+")
        print(f"[ingestion_manager] City selected: {city}")
        url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={COUNTRY_NAME}&key={API_KEY}"
        response = requests.get(url, timeout=15).json()
        send_to_logstash(LOGSTASH_HOSTNAME, LOGSTASH_PORT, response)
        time.sleep(10)


def get_demo_data() -> dict:
    """
    Retrieves all demo data from a given json file.
    """
    with open(file='demo_data.json', mode='r', encoding='utf-8') as f:
        return json.load(f)


async def demo() -> None:
    """
    Demo function to test the data ingestion process.
    """
    demo_data = get_demo_data()
    for element in demo_data:
        send_to_logstash(LOGSTASH_HOSTNAME, LOGSTASH_PORT, element)
    


if __name__ == '__main__':
    if not check_api_key():
        print ("[ingestion_manager] API_KEY environment variable not set!!")
        sys.exit()
    print("[ingestion_manager] API_KEY is set 👌")

    test_logstash()

    try:
        match DATA_ACTION:
            case "DEMO":
                asyncio.run(demo())
            case "NODEMO":
                asyncio.run(main())
            case _:
                send_to_logstash(LOGSTASH_HOSTNAME, LOGSTASH_PORT, get_data_handler())
    
    except KeyboardInterrupt:
        print("[ingestion-manager] Program exited")
