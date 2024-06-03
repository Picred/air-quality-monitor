import asyncio
import json
import sys
import time
import socket
from pylogbeat import PyLogBeatClient #type: ignore
from utils.extract_data import extract_data
from utils.retrieve_data import (
    get_states_by_country,
    get_cities_by_state_country,
    make_request,
    get_data,
    check_api_key
)
from utils.setup import logger, config, LOGSTASH_HOSTNAME, LOGSTASH_PORT


class LogstashHandler:
    """
    A class for handling communication with Logstash.
    Args:
        host (str): The hostname or IP address of the Logstash server.
        port (int): The port number on which Logstash is running.
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def test_logstash(self):
        """
        Checks if Logstash is ready for receiving data.
        """
        while True:
            try:
                with socket.create_connection((self.host, self.port)):
                    logger.info("Logstash is ready!")
                    break
            except socket.error:
                logger.warning("Logstash not ready, waiting... [CTRL+C to stop]")
                time.sleep(5)

    def send_to_logstash(self, data: dict):
        """
        Sends data to Logstash for ingestion.

        Args:
            data (dict): The data to be sent to Logstash.
        """
        if isinstance(data.get("data"), list):
            logger.info("Data to be sent: %s", data)
            return

        data = extract_data(data)
        client = PyLogBeatClient(self.host, self.port)
        client.send([json.dumps(data)])
        logger.info("Sent to Logstash! 🚀")


async def retrieve_and_send_data(logstash_handler: LogstashHandler):
    """
    Retrieves and sends air quality data to Logstash.

    Args:
        logstash_handler (LogstashHandler): The handler for sending data to Logstash.
    """
    logger.info("Starting data ingestion process...")
    logger.info("This is not a demo. Real data will be retrieved. It may take a while. 🕒")
    logger.info("Selected country: %s", config['COUNTRY_NAME'])
    logger.info("Retrieving data of major cities...")

    states = get_states_by_country(config['COUNTRY_NAME'])
    states_list = [elem['state'] for elem in states]

    time.sleep(1)

    for state in states_list:
        state = state.replace(" ", "+")
        logger.info("State retrieved: %s", state)
        cities = get_cities_by_state_country(state, config['COUNTRY_NAME'])

        if not cities:
            continue

        cities_list = [elem['city'] for elem in cities if 'city' in elem]
        if not cities_list:
            logger.warning("No cities found for this state. Maybe too many requests.\
                            Waiting 10 sec. [CTRL+C to stop]")
            time.sleep(10)
            continue

        logger.info("Retrieved cities %s", cities_list)
        time.sleep(10)

        city = cities_list[0].replace(" ", "+")
        logger.info("City selected: %s", city)
        url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country=\
            {config['COUNTRY_NAME']}&key={config['API_KEY']}"
        response = make_request(url)

        logstash_handler.send_to_logstash(response)
        time.sleep(10)


def get_demo_data() -> dict:
    """
    Retrieves all demo data from a given json file.
    """
    with open(file='demo_data.json', mode='r', encoding='utf-8') as f:
        return json.load(f)


async def demo(logstash_handler: LogstashHandler):
    """
    Demo function to test the data ingestion process.

    Args:
        logstash_handler (LogstashHandler): The handler for sending data to Logstash.
    """
    demo_data = get_demo_data()
    for element in demo_data:
        logstash_handler.send_to_logstash(element.get("data"))


async def main():
    """
    The main asynchronous function for executing the script.
    """
    logstash_handler = LogstashHandler(LOGSTASH_HOSTNAME, LOGSTASH_PORT)
    logstash_handler.test_logstash()

    data_action = config.get('DATA_ACTION', 'NODEMO')
    if data_action == "DEMO":
        await demo(logstash_handler)
    elif data_action == "NODEMO":
        await retrieve_and_send_data(logstash_handler)
    else:
        logstash_handler.send_to_logstash(get_data())


if __name__ == '__main__':
    if not check_api_key():
        logger.error("API_KEY environment variable not set!!")
        sys.exit(1)
    logger.info("API_KEY is set 👌")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program exited")
