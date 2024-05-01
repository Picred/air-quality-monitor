def extract_data(data_raw: dict) -> dict:
    """
    Extracts relevant air quality data from the HTML data_raw.

    Args:
        source (str): The HTML source containing air quality information.

    Returns:
        dict: A dictionary containing extracted air quality data.
    """
    clean_data = {
        "city" : data_raw.get("city"),
        "state" : data_raw.get("state"),
        "country" : data_raw.get("country"),
        "gps_lat" : data_raw.get("location").get("coordinates")[0],
        "gps_lon" : data_raw.get("location").get("coordinates")[1],
        "pollution_timestamp" : data_raw.get("current").get("pollution").get("ts"),
        "aqius" : data_raw.get("current").get("pollution").get("aqius"),
        "mainus" : data_raw.get("current").get("pollution").get("mainus"),
        "aqicn" : data_raw.get("current").get("pollution").get("aqicn"),
        "maincn" : data_raw.get("current").get("pollution").get("maincn"),
        "weather_timestamp" : data_raw.get("current").get("weather").get("ts"),
        "temperature" : data_raw.get("current").get("weather").get("tp"),
        "pression" : data_raw.get("current").get("weather").get("pr"),
        "humidity" : data_raw.get("current").get("weather").get("hu"),
        "wind_speed" : data_raw.get("current").get("weather").get("ws"),
        "wind_direction" : data_raw.get("current").get("weather").get("wd"),
        "icon" : data_raw.get("current").get("weather").get("ic")
    }
    return clean_data