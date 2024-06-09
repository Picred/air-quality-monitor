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
    "DATA_ACTION": os.getenv("DATA_ACTION", "NODEMO"),
    "cities" : ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo', 'Genoa', 'Bologna', 'Florence', 'Bari', 'Catania'],
    "scan_interval" : 2400 # ms
}

