import csv
import os
from .setup import logger

class CSVHandler:
    """
    A class for handling CSV file operations.
    Args:
        file_path (str): The file path where CSV data will be saved.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.fieldnames = ['aqi', 'city', 'co', 'lat', 'lon', 'nh3', 'no', 'no2', 'pm10', 'pm2_5', 'so2', 'timestamp_utc'] 

    def write_to_csv(self, data):
        """
        Write data to a CSV file.

        Args:
            data (dict): The data to be written to the CSV file.
        """
        logger.info("Data to write: %s", data)

        file_exists = os.path.isfile(self.file_path)
        write_header = not file_exists or os.stat(self.file_path).st_size == 0

        with open(self.file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            
            if write_header:
                writer.writeheader()

            writer.writerow(data)
            logger.info("Data written to CSV file.")
