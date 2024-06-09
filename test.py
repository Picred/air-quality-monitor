import json
import pandas as pd

# Load the CSV data
file_path = '/mnt/data/test_data.csv'
csv_data = pd.read_csv(file_path)

# Original JSON data
original_json = [
    {
        "status": "success",
        "data": {
            "country": "Italy",
            "location": {
                "type": "Point",
                "coordinates": [
                    15.07041,
                    37.49223
                ]
            },
            "state": "Sicily",
            "current": {
                "pollution": {
                    "aqicn": 16,
                    "mainus": "p2",
                    "maincn": "p2",
                    "aqius": 54,
                    "ts": "2024-05-12T12:00:00.000Z"
                },
                "weather": {
                    "wd": 70,
                    "pr": 1016,
                    "ic": "01d",
                    "ts": "2024-05-12T13:00:00.000Z",
                    "tp": 23,
                    "hu": 49,
                    "ws": 5.14
                }
            },
            "city": "Catania"
        }
    },
    {
        "status": "success",
        "data": {
            "city": "Rome",
            "state": "Latium",
            "country": "Italy",
            "location": {
                "type": "Point",
                "coordinates": [12.4509, 41.9089]
            },
            "current": {
                "pollution": {
                    "ts": "2024-05-23T10:00:00.000Z",
                    "aqius": 23,
                    "mainus": "p2",
                    "aqicn": 16,
                    "maincn": "n2"
                },
                "weather": {
                    "ts": "2024-05-23T10:00:00.000Z",
                    "tp": 22,
                    "pr": 1018,
                    "hu": 48,
                    "ws": 4.63,
                    "wd": 210,
                    "ic": "02d"
                }
            }
        }
    },
    {
        "status": "success",
        "data": {
            "city": "Milano",
            "state": "Lombardy",
            "country": "Italy",
            "location": {
                "type": "Point",
                "coordinates": [9.19746075, 45.470501]
            },
            "current": {
                "pollution": {
                    "ts": "2024-05-23T09:00:00.000Z",
                    "aqius": 22,
                    "mainus": "p2",
                    "aqicn": 6,
                    "maincn": "p2"
                },
                "weather": {
                    "ts": "2024-05-23T09:00:00.000Z",
                    "tp": 16,
                    "pr": 1016,
                    "hu": 82,
                    "ws": 1.54,
                    "wd": 30,
                    "ic": "03d"
                }
            }
        }
    },
    {
        "status": "success",
        "data": {
            "city": "Naples",
            "state": "Campania",
            "country": "Italy",
            "location": {
                "type": "Point",
                "coordinates": [14.25451, 40.863690000000005]
            },
            "current": {
                "pollution": {
                    "ts": "2024-05-23T09:00:00.000Z",
                    "aqius": 55,
                    "mainus": "p2",
                    "aqicn": 25,
                    "maincn": "p1"
                },
                "weather": {
                    "ts": "2024-05-23T10:00:00.000Z",
                    "tp": 22,
                    "pr": 1014,
                    "hu": 61,
                    "ws": 8.49,
                    "wd": 277,
                    "ic": "03d"
                }
            }
        }
    },
    {
        "status": "success",
        "data": {
            "city": "Brindisi",
            "state": "Apulia",
            "country": "Italy",
            "location": {
                "type": "Point",
                "coordinates": [17.93833, 40.63806]
            },
            "current": {
                "pollution": {
                    "ts": "2024-05-23T07:00:00.000Z",
                    "aqius": 53,
                    "mainus": "p2",
                    "aqicn": 14,
                    "maincn": "p2"
                },
                "weather": {
                    "ts": "2024-05-23T10:00:00.000Z",
                    "tp": 21,
                    "pr": 1017,
                    "hu": 73,
                    "ws": 5.66,
                    "wd": 340,
                    "ic": "01d"
                }
            }
        }
    },
    {
        "status": "success",
        "data": {
            "city": "Florence",
            "state": "Tuscany",
            "country": "Italy",
            "location": {
                "type": "Point",
                "coordinates": [11.27222, 43.77306]
            },
            "current": {
                "pollution": {
                    "ts": "2024-05-23T09:00:00.000Z",
                    "aqius": 49,
                    "mainus": "p2",
                    "aqicn": 13,
                    "maincn": "p2"
                },
                "weather": {
                    "ts": "2024-05-23T10:00:00.000Z",
                    "tp": 21,
                    "pr": 1018,
                    "hu": 59,
                    "ws": 2.06,
                    "wd": 0,
                    "ic": "03d"
                }
            }
        }
    },
    {
        "status": "success",
        "data": {
            "city": "La Spezia",
            "state": "Liguria",
            "country": "Italy",
            "location": {
                "type": "Point",
                "coordinates": [9.82375, 44.103]
            },
            "current": {
                "pollution": {
                    "ts": "2024-05-23T09:00:00.000Z",
                    "aqius": 26,
                    "mainus": "p2",
                    "aqicn": 7,
                    "maincn": "p2"
                },
                "weather": {
                    "ts": "2024-05-23T10:00:00.000Z",
                    "tp": 18,
                    "pr": 1015,
                    "hu": 75,
                    "ws": 1.79,
                    "wd": 158,
                    "ic": "03d"
                }
            }
        }
    },
    {
        "status": "success",
        "data": {
            "city": "Torino",
            "state": "Piedmont",
            "country": "Italy",
            "location": {
                "type": "Point",
                "coordinates": [7.682645, 45.058575]
            },
            "current": {
                "pollution": {
                    "ts": "2024-05-23T08:00:00.000Z",
                    "aqius": 18,
                    "mainus": "o3",
                    "aqicn": 17,
                    "maincn": "n2"
                },
                "weather": {
                    "ts": "2024-05-23T10:00:00.000Z",
                    "tp": 17,
                    "pr": 1015,
                    "hu": 73,
                    "ws": 4.63,
                    "wd": 80,
                    "ic": "04d"
                }
            }
        }
    },
    {
        "status": "success",
        "data": {
            "city": "Bologna",
            "state": "Emilia-Romagna",
            "country": "Italy",
            "location": {
                "type": "Point",
                "coordinates": [11.355000000000002, 44.48333]
            },
            "current": {
                "pollution": {
                    "ts": "2024-05-23T07:00:00.000Z",
                    "aqius": 34,
                    "mainus": "o3",
                    "aqicn": 26,
                    "maincn": "o3"
                },
                "weather": {
                    "ts": "2024-05-23T10:00:00.000Z",
                    "tp": 23,
                    "pr": 1015,
                    "hu": 49,
                    "ws": 1.79,
                    "wd": 79,
                    "ic": "02d"
                }
            }
        }
    },
    {
        "status": "success",
        "data": {
            "city": "Cagliari",
            "state": "Sardinia",
            "country": "Italy",
            "location": {
                "type": "Point",
                "coordinates": [9.11917, 39.23054]
            },
            "current": {
                "pollution": {
                    "ts": "2024-05-23T02:00:00.000Z",
                    "aqius": 77,
                    "mainus": "p2",
                    "aqicn": 33,
                    "maincn": "p2"
                },
                "weather": {
                    "ts": "2024-05-23T10:00:00.000Z",
                    "tp": 25,
                    "pr": 1017,
                    "hu": 36,
                    "ws": 3.09,
                    "wd": 300,
                    "ic": "01d"
                }
            }
        }
    },
    {
        "status": "success",
        "data": {
            "city": "Verona",
            "state": "Veneto",
            "country": "Italy",
            "location": {
                "type": "Point",
                "coordinates": [10.96389, 45.44528]
            },
            "current": {
                "pollution": {
                    "ts": "2024-05-23T10:00:00.000Z",
                    "aqius": 49,
                    "mainus": "p2",
                    "aqicn": 13,
                    "maincn": "p2"
                },
                "weather": {
                    "ts": "2024-05-23T10:00:00.000Z",
                    "tp": 21,
                    "pr": 1011,
                    "hu": 67,
                    "ws": 2.06,
                    "wd": 0,
                    "ic": "03d"
                }
            }
        }
    }
]

# Function to convert CSV row to JSON
def row_to_json(row):
    return {
        "status": "success",
        "data": {
            "city": row['city'],
            "state": row['state'],
            "country": row['country'],
            "location": {
                "type": "Point",
                "coordinates": [row['gps_lon'], row['gps_lat']]
            },
            "current": {
                "pollution": {
                    "ts": row['pollution_timestamp'],
                    "aqius": row['aqius'],
                    "mainus": row['mainus'],
                    "aqicn": row['aqicn'],
                    "maincn": row['maincn']
                },
                "weather": {
                    "ts": row['weather_timestamp'],
                    "tp": row['temperature'],
                    "pr": row['pression'],
                    "hu": row['humidity'],
                    "ws": row['wind_speed'],
                    "wd": row['wind_direction'],
                    "ic": row['icon']
                }
            }
        }
    }

# Convert CSV data to JSON format and add to original JSON
for index, row in csv_data.iterrows():
    original_json.append(row_to_json(row))

# Convert the updated JSON list to a string
json_output = json.dumps(original_json, indent=4)

# Display the output
print(json_output)