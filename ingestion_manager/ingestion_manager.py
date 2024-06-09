import asyncio
import sys
import time
from utils.retrieve_data import (
    make_request,
    get_coord,
    check_api_key
)
from utils.setup import logger, config
from utils.logstash_handler import LogstashHandler
from utils.train_data import CSVHandler
from utils.extract_data import extract_data


async def retrieve_and_send_data(logstash_handler: LogstashHandler, csv_handler: CSVHandler):
    """
    Retrieves and sends air quality data to Logstash.

    Args:
        logstash_handler (LogstashHandler): The handler for sending data to Logstash.
    """
    logger.info("Starting data ingestion process...")
    logger.info("This is not a demo. Real data will be retrieved. It may take a while. 🕒")
    logger.info("Retrieving data of major cities of Italy...")

    cities_list = config['cities']

    for city in cities_list:
        coordinates = get_coord(city)
        
        if coordinates.get('error'):
            logger.error(f"Error: {coordinates.get('error')}")
            continue
        else:
            logger.info(f"Retrieving data for {city}...")
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={coordinates.get('lat')}&lon={coordinates.get('lat')}&appid={config['API_KEY']}"

        response = make_request(url)
        response = extract_data(response, city)
        time.sleep(15)

        if csv_handler:
            csv_handler.write_to_csv(response)
        else:
            logstash_handler.send_to_logstash(response)

async def main():
    """
    The main asynchronous function for executing the script.
    """
    match config['DATA_ACTION']:
        case "NODEMO":
            logstash_handler = LogstashHandler(config['LOGSTASH_HOSTNAME'], config['LOGSTASH_PORT'])
            logstash_handler.test_logstash()
            await retrieve_and_send_data(logstash_handler=logstash_handler, csv_handler=None)
            pass
        case "TRAIN_MODEL":
            csv_handler = CSVHandler("/opt/aqm/ingestion_manager/data/historical_data.csv")
            await retrieve_and_send_data(logstash_handler=None, csv_handler=csv_handler)          
            pass
        case _:
            logger.error("Invalid data action. Exiting...")
            sys.exit(1)

if __name__ == '__main__':
    if not check_api_key():
        logger.error("API_KEY environment variable not set!!")
        sys.exit(1)
    logger.info("API_KEY is set 👌")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program exited")
