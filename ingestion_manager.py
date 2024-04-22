import asyncio
import json
import sys
import time
import socket
import os
import bs4
import requests

API_KEY = os.getenv("API_KEY", None)
COUNTRY_NAME = os.getenv("COUNTRY_NAME", "Italy")
STATE_NAME = os.getenv("STATE_NAME", "Sicily")
GPS_LAT = int(os.getenv("GPS_LAT", "37.500000"))
GPS_LON = int(os.getenv("GPS_LON", "15.090278"))
CITY_TO_SCAN = os.getenv("CITY_TO_SCAN", "Catania")
DATA_ACTION = os.getenv("DATA_ACTION", "NEAREST_IP_CITY")

ALL_COUNTRIES_URL = f"http://api.airvisual.com/v2/countries?key={API_KEY}"
ALL_STATES_BY_COUNTRY_URL = f"http://api.airvisual.com/v2/states?country={COUNTRY_NAME}&key={API_KEY}" # pylint: disable=line-too-long
ALL_CITIES_BY_STATECOUNTRY_URL = f"http://api.airvisual.com/v2/cities?state={STATE_NAME}&country={COUNTRY_NAME}&key={API_KEY}"
NEAREST_IP_CITY_URL = f"http://api.airvisual.com/v2/nearest_city?key={API_KEY}"
NEAREST_GPS_CITY_URL = f"http://api.airvisual.com/v2/nearest_city?lat={GPS_LAT}&lon={GPS_LON}&key={API_KEY}"

def get_data() -> str:
    """
    Retrieves weather data based on the specified action.

    Returns:
        str: The response text containing weather data.
    """
    match DATA_ACTION:
        case "ALL_COUNTRIES":
            return requests.get(f"{ALL_COUNTRIES_URL}", timeout=15).text
        case "ALL_STATES_BY_COUNTRY":
            return requests.get(f"{ALL_STATES_BY_COUNTRY_URL}", timeout=15).text
        case "ALL_CITIES_BY_STATECOUNTRY":
            return requests.get(f"{ALL_CITIES_BY_STATECOUNTRY_URL}", timeout=15).text
        case "NEAREST_IP_CITY":
            return requests.get(f"{NEAREST_IP_CITY_URL}", timeout=15).text
        case "NEAREST_GPS_CITY":
            return requests.get(f"{NEAREST_GPS_CITY_URL}", timeout=15).text

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



def extract_data(source: str) -> dict:
    """
    Extracts relevant weather data from the HTML source.

    Args:
        source (str): The HTML source containing weather information.

    Returns:
        dict: A dictionary containing extracted weather data.
    """
    soup=bs4.BeautifulSoup(source, 'lxml')

    weather = soup.find("div", {"class": "current-conditions-card content-module non-ad"})

    data = {
        'LocationTime': weather.find("p", {"class": "module-header sub date"}).next,
        'WeatherText': weather.find("div", {"class": "phrase"}).next,
        'Temperature': {
            'Unit': "C"
        },
        'RealFeelTemperature': {
            'Unit': "C"
        },
        'RealFeelTemperatureShade': {
            'Unit': "C"
        }
    }
    return data

def test_logstash() -> None:
    """
    Checks if Logstash is ready for receiving data.
    """
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('logstash', 5000))
            sock.close()
            print("[ingestion_manager]Logstash is ready!")
            break
        except socket.error:
            print("[ingestion_manager]Logstash not ready, waiting...")
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
    print("continuo")

    data_raw = get_data()

    extract_data(data_raw)






if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[ingestion-manager]Program exited")
