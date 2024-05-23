import json

with open(file='demo_data.json', mode='r', encoding='utf-8') as f:
    data = json.load(f)

# print(data[0].get("data").keys())

print(type(data[0]) == list)