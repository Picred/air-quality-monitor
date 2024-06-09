"""Sets up the configuration and URLs for the ingestion manager."""
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingestion_manager")

# Configuration
config = {
    "LOGSTASH_PORT": 5044,
    "LOGSTASH_HOSTNAME": "logstash",
    "API_KEY": os.getenv("API_KEY", "056928b3fb7012b32cfa961ddd30a609"),
    "DATA_ACTION": os.getenv("DATA_ACTION", "NODEMO"),
    "cities" : ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo', 'Genoa', 'Bologna', 'Florence', 'Bari',
                    'Catania', 'Florence', 'Venice', 'Verona', 'Messina', 'Padua', 'Trieste', 'Brescia',
                    'Taranto', 'Prato', 'Reggio Calabria', 'Modena', 'Parma', 'Perugia', 'Livorno',
                    'Ravenna', 'Foggia', 'Rimini', 'Salerno', 'Ferrara', 'Sassari', 'Latina', 'Giugliano in Campania',
                    'Monza', 'Syracuse', 'Bergamo', 'Pescara', 'Forlì', 'Trento', 'Vicenza', 'Terni', 'Bolzano', 'Novara',
                    'Piacenza', 'Ancona', 'Andria', 'Udine', 'Arezzo', 'Cesena', 'Lecce', 'Pesaro', 'Barletta', 'Alessandria',
                    'La Spezia', 'Pisa', 'Pistoia', 'Guidonia Montecelio', 'Lucca', 'Mestre', 'Catanzaro', 'Udine', 'Brindisi',
                    'Busto Arsizio', 'Como', 'Cosenza', 'Gela', 'Cinisello Balsamo', 'Molfetta', 'Aversa', 'Civitavecchia', 'Caserta',
                    'Asti', 'Crotone', 'Casoria', 'Savona', 'Velletri', 'Carrara', 'Caltanissetta', 'Viareggio', 'Sesto San Giovanni',
                    'Fano', 'Massa', 'Trapani', 'Legnano', 'Potenza', 'Castellammare di Stabia', 'Imola', 'Cerignola', 'Vittoria', 'Vigevano',
                    'Cuneo', 'Gallarate', 'Faenza', 'Marano di Napoli', 'Sanremo', 'Carpi', 'Afragola', 'Bagheria', 'Manfredonia', 'Sassuolo',
                    'Caltagirone', 'Bitonto', 'Portici', 'Avellino', 'Acerra', 'Mazara del Vallo', 'Ragusa', 'Chieti', 'Trani', 'Bisceglie','Ercolano'
                ],
    "scan_interval" : 2400 # ms
}

