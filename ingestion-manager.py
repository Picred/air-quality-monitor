import asyncio
import time, socket
import requests
import os
from dotenv import dotenv_values

#config = dotenv_values()

API_KEY = os.getenv("API_KEY", None)
COUNTRY_NAME = os.getenv("COUNTRY_NAME", "Italy")
STATE_NAME = os.getenv("STATE_NAME", "Sicily")
GPS_LAT = os.getenv("GPS_LAT", 37.500000)
GPS_LON = os.getenv("GPS_LON", 15.090278)
CITY_TO_SCAN = os.getenv("CITY_TO_SCAN", "Catania")
DATA_ACTION = os.getenv("DATA_ACTION", "NEAREST_IP_CITY")

ALL_COUNTRIES_URL = f"http://api.airvisual.com/v2/countries?key={API_KEY}"
ALL_STATES_BY_COUNTRY_URL = f"http://api.airvisual.com/v2/states?country={COUNTRY_NAME}&key={API_KEY}"
ALL_CITIES_BY_STATECOUNTRY_URL = f"http://api.airvisual.com/v2/cities?state={STATE_NAME}&country={COUNTRY_NAME}&key={API_KEY}"
NEAREST_IP_CITY_URL = f"http://api.airvisual.com/v2/nearest_city?key={API_KEY}"
NEAREST_GPS_CITY_URL = f"http://api.airvisual.com/v2/nearest_city?lat={GPS_LAT}&lon={GPS_LON}&key={API_KEY}"
# SPECIFIED_CITY_URL = f"http://api.airvisual.com/v2/city?city={CITY_TO_SCAN}&state={STATE_NAME}&country={COUNTRY_NAME}&key={API_KEY}"



def test_logstash() -> None:
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('logstash', 5000))
            sock.close()
            print("[ingestion-manager]Logstash is ready!")
            break
        except:
            print("[ingestion-manager]Logstash not ready, waiting...")
            time.sleep(5)
            continue


def check_api_key() -> bool:
    return True if API_KEY is not None else False


async def main() -> None:
    if not check_api_key():
        print (f"[ingestion-manager] API_KEY environment variable not set!!")
        exit()
    print("continuo")

    data_json = None
    
    match DATA_ACTION:
        case "ALL_COUNTRIES":
            data_json = print(requests.get(f"{ALL_COUNTRIES_URL}").text)
        case "ALL_STATES_BY_COUNTRY":
            data_json = print(requests.get(f"{ALL_STATES_BY_COUNTRY_URL}").text)
        case "ALL_CITIES_BY_STATECOUNTRY":
            data_json = print(requests.get(f"{ALL_CITIES_BY_STATECOUNTRY_URL}").text)
        case "NEAREST_IP_CITY":
            data_json = print(requests.get(f"{NEAREST_IP_CITY_URL}").text)
        case "NEAREST_GPS_CITY":
            data_json = print(requests.get(f"{NEAREST_GPS_CITY_URL}").text)


#    test_logstash()



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[ingestion-manager]Program exited")
