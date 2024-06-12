"""Sets up the configuration and URLs for the ingestion manager."""
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingestion_manager")

config = {
    "LOGSTASH_PORT": 5044,
    "LOGSTASH_HOSTNAME": "logstash",
    "API_KEY": os.getenv("API_KEY", "056928b3fb7012b32cfa961ddd30a609"),
    "cities" : [ # 'Gela',
        'Rome', 'Milan', 'Naples', 'Turin', 'Palermo', 'Genoa', 'Bologna', 'Florence', 'Bari','Catania', 
        'Florence', 'Venice', 'Verona', 'Messina', 'Padua', 'Trieste', 'Brescia', 'Taranto', 'Prato', 'Reggio Calabria',
        'Modena', 'Parma', 'Perugia', 'Livorno', 'Ravenna', 'Foggia', 'Rimini', 'Salerno', 'Ferrara', 'Sassari', 'Latina',
    ],
    "scan_interval" : 15 # seconds
}
