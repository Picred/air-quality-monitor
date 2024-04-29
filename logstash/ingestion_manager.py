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

API_KEY = os.getenv("API_KEY", None)
COUNTRY_NAME = os.getenv("COUNTRY_NAME", "Italy")
STATE_NAME = os.getenv("STATE_NAME", "Sicily")
GPS_LAT = float(os.getenv("GPS_LAT", "37.500000"))
GPS_LON = float(os.getenv("GPS_LON", "15.090278"))
CITY_TO_SCAN = os.getenv("CITY_TO_SCAN", "Catania")
DATA_ACTION = os.getenv("DATA_ACTION", "NEAREST_IP_CITY")

ALL_COUNTRIES_URL = f"http://api.airvisual.com/v2/countries?key={API_KEY}"
ALL_STATES_BY_COUNTRY_URL = f"http://api.airvisual.com/v2/states?country={COUNTRY_NAME}&key={API_KEY}" # pylint: disable=line-too-long
ALL_CITIES_BY_STATECOUNTRY_URL = f"http://api.airvisual.com/v2/cities?state={STATE_NAME}&country={COUNTRY_NAME}&key={API_KEY}"
NEAREST_IP_CITY_URL = f"http://api.airvisual.com/v2/nearest_city?key={API_KEY}"
NEAREST_GPS_CITY_URL = f"http://api.airvisual.com/v2/nearest_city?lat={GPS_LAT}&lon={GPS_LON}&key={API_KEY}"


def get_data() -> dict:
    """
    Retrieves air quality data based on the specified action.

    Returns:
        dict: The json response containing air quality data.
    """
    match DATA_ACTION:
        case "ALL_COUNTRIES":
            return requests.get(f"{ALL_COUNTRIES_URL}", timeout=15).json()
        case "ALL_STATES_BY_COUNTRY":
            return requests.get(f"{ALL_STATES_BY_COUNTRY_URL}", timeout=15).json()
        case "ALL_CITIES_BY_STATECOUNTRY":
            return requests.get(f"{ALL_CITIES_BY_STATECOUNTRY_URL}", timeout=15).json()
        case "NEAREST_IP_CITY":
            return requests.get(f"{NEAREST_IP_CITY_URL}", timeout=15).json()
        case "NEAREST_GPS_CITY":
            return requests.get(f"{NEAREST_GPS_CITY_URL}", timeout=15).json()


def send_to_logstash(host: str, port: int, data: dict):
    """
    Sends data to Logstash for ingestion.

    Args:
        host (str): The hostname or IP address of the Logstash server.
        port (int): The port number of the Logstash server.
        data (dict): The data to be sent to Logstash.
    """
    error = True
    while error:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket created. sock: " + str(sock))

            sock.connect((host, port))
            print("Socket connected to HOST: " + host + " PORT: " + str(port))
            print("Socket connected. Sock: " + str(sock))

            print("Sending message: " + str(data))

            sock.sendall(json.dumps(data).encode())
            print("End connection")
            sock.close()
            error = False
        except socket.error:
            print("Connection error. There will be a new attempt in 10 seconds")
            time.sleep(10)



def extract_data(data_raw: dict) -> dict:
    """
    Extracts relevant air quality data from the HTML data_raw.

    Args:
        source (str): The HTML source containing air quality information.

    Returns:
        dict: A dictionary containing extracted air quality data.
    """
    clean_data = {
        "city" : data_raw.get("city"),
        "state" : data_raw.get("state"),
        "country" : data_raw.get("country"),
        "gps_lat" : data_raw.get("location").get("coordinates")[0],
        "gps_lon" : data_raw.get("location").get("coordinates")[1],
        "pollution_timestamp" : data_raw.get("current").get("pollution").get("ts"),
        "aqius" : data_raw.get("current").get("pollution").get("aqius"),
        "mainus" : data_raw.get("current").get("pollution").get("mainus"),
        "aqicn" : data_raw.get("current").get("pollution").get("aqicn"),
        "maincn" : data_raw.get("current").get("pollution").get("maincn"),
        "weather_timestamp" : data_raw.get("current").get("weather").get("ts"),
        "tp" : data_raw.get("current").get("weather").get("tp"),
        "pr" : data_raw.get("current").get("weather").get("pr"),
        "hu" : data_raw.get("current").get("weather").get("hu"),
        "ws" : data_raw.get("current").get("weather").get("ws"),
        "wd" : data_raw.get("current").get("weather").get("wd"),
        "ic" : data_raw.get("current").get("weather").get("ic")
    }
    return clean_data


def test_logstash() -> None:
    """
    Checks if Logstash is ready for receiving data.
    """
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('logstash', 5044))
            sock.close()
            print("[ingestion_manager]Logstash is ready!")
            break
        except socket.error:
            print("[ingestion_manager]Logstash not ready, waiting... [CTRL+C to stop]")
            time.sleep(5)
            continue


def check_api_key() -> bool:
    """
    Checks if the API key is set.

    Returns:
        bool: True if API key is set, False otherwise.
    """
    return API_KEY is not None



async def main() -> None:
    """
    The main asynchronous function for executing the script.
    """
    if not check_api_key():
        print ("[ingestion_manager] API_KEY environment variable not set!!")
        sys.exit()
    print("[ingestion_manager] API_KEY is set 👌")

    test_logstash()

    print(f"[ingestion_manager] Main Information\nCountry: {COUNTRY_NAME}")
    print(f"State: {STATE_NAME}")
    print(f"Latitude: {GPS_LAT}")
    print(f"Longitude: {GPS_LON}")
    print(f"Selected city to scan: {CITY_TO_SCAN} ")
    print(f"Action selected: {DATA_ACTION}")
    print("Use Environment Variables to change values (See more on README.md)\n")

    data_raw = get_data()

    if not data_raw.get("status") == "success":
        print ("[ingestion_manager] Server error while getting data!")
        sys.exit()

    clean_data = extract_data(data_raw.get("data"))

    send_to_logstash("logstash", 5000, clean_data)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[ingestion-manager] Program exited")
