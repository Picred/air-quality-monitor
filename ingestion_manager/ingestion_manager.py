import asyncio
import sys
import time
from utils.retrieve_data import (
    make_request,
    get_coord,
    check_api_key
)
from utils.setup import logger, config, LOGSTASH_HOSTNAME, LOGSTASH_PORT
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
    logger.info("Retrieving data of major cities...")

    cities_list = config['cities']


    for city in cities_list:
        coordinates = get_coord(city)
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={coordinates.get('lat')}&lon={coordinates.get('lat')}&appid={config['API_KEY']}"
        
        response = make_request(url)
        
        response = extract_data(response, city)
        
        time.sleep(10)

    # if csv_handler:
    #     csv_handler.write_to_csv(response)
    # else:
        logstash_handler.send_to_logstash(response)

    # time.sleep(10)


async def main():
    """
    The main asynchronous function for executing the script.
    """
    csv_handler = CSVHandler("/ingestion_manager/data/historical_data.csv")

    logstash_handler = LogstashHandler(LOGSTASH_HOSTNAME, LOGSTASH_PORT)
    # logstash_handler.test_logstash() # Comment to get data for training

    data_action = config['DATA_ACTION']
    if data_action == "NODEMO":
        await retrieve_and_send_data(logstash_handler=logstash_handler, csv_handler=None) # Comment to get data for training
        # await retrieve_and_send_data(logstash_handler=None, csv_handler=csv_handler) # Uncomment to train data


if __name__ == '__main__':
    if not check_api_key():
        logger.error("API_KEY environment variable not set!!")
        sys.exit(1)
    logger.info("API_KEY is set 👌")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program exited")
