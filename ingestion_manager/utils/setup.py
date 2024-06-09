"""Sets up the configuration and URLs for the ingestion manager."""
import logging
import os

LOGSTASH_PORT = 5044
LOGSTASH_HOSTNAME = "logstash"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingestion_manager")

# Configuration
config = {
    "API_KEY": os.getenv("API_KEY", "056928b3fb7012b32cfa961ddd30a609"),
    "COUNTRY_NAME": os.getenv("COUNTRY_NAME", "Italy"),
    "GPS_LAT": float(os.getenv("GPS_LAT", "37.500000")),
    "GPS_LON": float(os.getenv("GPS_LON", "15.090278")),
    "CITY_TO_SCAN": os.getenv("CITY_TO_SCAN", "Catania"),
    "STATE_NAME": os.getenv("STATE_NAME", "Sicily"),
    "DATA_ACTION": os.getenv("DATA_ACTION", "NODEMO"),
    "cities" : ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo', 'Genoa', 'Bologna', 'Florence', 'Bari', 'Catania']
}

# URLs
URLS = {
    "ALL_COUNTRIES": f"http://api.airvisual.com/v2/countries?key={config['API_KEY']}",
    "ALL_STATES_BY_COUNTRY": f"http://api.airvisual.com/v2/states?country=\
            {config['COUNTRY_NAME']}&key={config['API_KEY']}",
    "ALL_CITIES_BY_STATE_COUNTRY": f"http://api.airvisual.com/v2/cities?state=\
            {config['STATE_NAME']}&country={config['COUNTRY_NAME']}&key={config['API_KEY']}",
    "NEAREST_IP_CITY": f"http://api.airvisual.com/v2/nearest_city?key={config['API_KEY']}",
    "NEAREST_GPS_CITY": f"http://api.airvisual.com/v2/nearest_city?lat=\
            {config['GPS_LAT']}&lon={config['GPS_LON']}&key={config['API_KEY']}",
    "SPECIFIC_CITY": f"http://api.airvisual.com/v2/city?city={config['CITY_TO_SCAN']}&state=\
            {config['STATE_NAME']}&country={config['COUNTRY_NAME']}&key={config['API_KEY']}",
}
