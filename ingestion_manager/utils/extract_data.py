"""Cleans raw data from GET request"""
import datetime

def extract_data(data_raw: dict, city: str) -> dict:
    """
    Extracts relevant air quality data from the HTML data_raw.

    Args:
        source (`str`): The HTML source containing air quality information.

    Returns:
        `dict`: A dictionary containing extracted air quality data.
    """
    clean_data = {
        "city" : city,
        "lat" : data_raw.get("coord").get("lat"),
        "lon" : data_raw.get("coord").get("lon"),
        "aqi" : data_raw.get("list")[0].get("main").get("aqi"),
        "timestamp_utc" : datetime.datetime.fromtimestamp(data_raw.get("list")[0].get("dt")).strftime('%Y-%m-%d %H:%M:%S'),
        "co" : data_raw.get("list")[0].get("components").get("co"),
        "no" : data_raw.get("list")[0].get("components").get("no"),
        "no2" : data_raw.get("list")[0].get("components").get("no2"),
        "so2" : data_raw.get("list")[0].get("components").get("so2"),
        "pm2_5" : data_raw.get("list")[0].get("components").get("pm2_5"),
        "nh3" : data_raw.get("list")[0].get("components").get("nh3"),
        "pm10" : data_raw.get("list")[0].get("components").get("pm10")
    }
    return clean_data
