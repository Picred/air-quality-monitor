# import datetime
# import requests

# # Timestamp Unix
# unix_timestamp = [1717941309, 1717941623, 1717942265, 1717942210]

# # Converti il timestamp in un oggetto datetime
# for i in unix_timestamp:
#     date_time = datetime.datetime.fromtimestamp(i)
#     print()
#     print(i)
#     print(date_time.strftime('%Y-%m-%d %H:%M:%S'))

# # http://api.openweathermap.org/data/2.5/air_pollution?lat=37.500000&lon=15.090278&appid=056928b3fb7012b32cfa961ddd30a609

# response = requests.get("http://api.openweathermap.org/data/2.5/air_pollution?lat=37.500000&lon=15.090278&appid=056928b3fb7012b32cfa961ddd30a609")

# print(response.json())


from geopy.geocoders import Nominatim

def get_coord(city):
    geolocator = Nominatim(user_agent="geoapiExercises")

    try:
        location = geolocator.geocode(city)
        if location:
            return {'latitude': location.latitude, 'longitude': location.longitude}
        else:
            return {'error': 'Location not found'}
    except Exception as e:
        return {'error': str(e)}

# Esempio di utilizzo

city = "Rome"
coordinates = get_coord(city)
print(coordinates)
