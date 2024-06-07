import csv
from .setup import logger
from .extract_data import extract_data

class CSVHandler:
    """
    A class for handling CSV file operations.
    Args:
        file_path (str): The file path where CSV data will be saved.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.fieldnames = ['city', 'state', 'country', 'gps_lat', 'gps_lon', 'pollution_timestamp', 'aqius', 'mainus', 'aqicn', 'maincn', 'weather_timestamp', 'temperature', 'pression', 'humidity', 'wind_speed', 'wind_direction', 'icon']
        # Write the header only once, during initialization
        with open(self.file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()

    def write_to_csv(self, data):
        """
        Write data to a CSV file.

        Args:
            data (dict): The data to be written to the CSV file.
        """
        # Check if 'data' is a list and log information
        if isinstance(data.get("data"), list):
            logger.info("Data to be written: %s", data)
            return

        # Extract data using the provided extract_data function
        extracted_data = extract_data(data)

        # Log the data to be written
        logger.info("Data to write: %s", extracted_data)

        # Write data to CSV file
        with open(self.file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow(extracted_data)
