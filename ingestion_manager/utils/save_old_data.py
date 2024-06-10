import datetime
import json
from csv_handler import CSVHandler


def extract_historic_data(data_raw: dict, city: str) -> dict:
    """
    Extracts relevant air quality data from the data_raw to train model.

    Args:
        source (`str`): The dictionary source containing air quality information.

    Returns:
        `dict`: A dictionary containing extracted air quality data.
    """
    clean_data = {
        "city" : city,
        "lat" : data_raw.get("coord").get("lat"),
        "lon" : data_raw.get("coord").get("lon"),
        "aqi" : data_raw.get("list").get("main").get("aqi"),
        "timestamp_utc" : datetime.datetime.fromtimestamp(data_raw.get("list").get("dt")).strftime('%Y-%m-%d %H:%M:%S'),
        "co" : data_raw.get("list").get("components").get("co"),
        "no" : data_raw.get("list").get("components").get("no"),
        "no2" : data_raw.get("list").get("components").get("no2"),
        "so2" : data_raw.get("list").get("components").get("so2"),
        "pm2_5" : data_raw.get("list").get("components").get("pm2_5"),
        "nh3" : data_raw.get("list").get("components").get("nh3"),
        "pm10" : data_raw.get("list").get("components").get("pm10")
    }
    return clean_data

if __name__ == "__main__":
    csv_handler = CSVHandler("../data/historical_data.csv")

    with open('../data/milan_3munths.json') as f:
        data_raw = json.load(f)

    for item in data_raw.get("list"):
        new_raw_data = {
            "coord" : data_raw.get("coord"),
            "list" : item
        }
        csv_handler.write_to_csv(extract_historic_data(new_raw_data, "Milan"))
