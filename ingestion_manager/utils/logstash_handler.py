import time
import socket
import json
from pylogbeat import PyLogBeatClient
from .setup import logger

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

        client = PyLogBeatClient(self.host, self.port)
        client.send([json.dumps(data)])
        logger.info("Sent to Logstash! 🚀")
