import requests
from ingestion_manager.utils.extract_data import extract_data
# Timestamp Unix
# unix_timestamp = [1717941309, 1717941623, 1717942265, 1717942210]

# # Converti il timestamp in un oggetto datetime
# for i in unix_timestamp:
#     date_time = datetime.datetime.fromtimestamp(i)
#     print()
#     print(i)
#     print(date_time.strftime('%Y-%m-%d %H:%M:%S'))



from geopy.geocoders import Nominatim

def get_coord(city):
    geolocator = Nominatim(user_agent="provami")

    location = geolocator.geocode(city)
    print(location)
    if location:
        return {'lat': location.latitude, 'lon': location.longitude}
    else:
        return {'error': 'Location not found'}

# Esempio di utilizzo

city = "Rome"
coordinates = get_coord(city)

url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={coordinates.get('lat')}&lon={coordinates.get('lat')}&appid=056928b3fb7012b32cfa961ddd30a609"

response = requests.get(url).json()

print(response)
print(extract_data(response, city))