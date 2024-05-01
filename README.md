# Real-time air quality tracking software


# Prerequisites
To use the Air-Flow Monitor, you should be familiar with the following:
- [Docker](https://www.docker.com/)
- [Python](https://www.python.org/)

# Setup

## Ingestion Manager
To execute the script within the container, environment variables must be set. Specifically, variables need to be configured based on the desired data collection:

`API_KEY` = Your [IQAIR](https://www.iqair.com) API key  
`DATA_ACTION =  ["ALL_COUNTRIES" | "ALL_STATES_BY_COUNTRY" | "ALL_CITIES_BY_STATECOUNTRY" | "NEAREST_IP_CITY" | "NEAREST_GPS_CITY"]`. Default value is `NEAREST_IP_CITY`


Below are the environment variables to be set according to the `DATA_ACTION`:
|DATA_ACTION|Dependencies|
|---|---|
|ALL_COUNTRIES|`API_KEY`|
|NEAREST_IP_CITY|`API_KEY`|
|ALL_STATES_BY_COUNTRY|`API_KEY`, `STATE_NAME`|
|ALL_CITIES_BY_STATE_COUNTRY|`API_KEY`, `STATE_NAME`, `COUNTRY_NAME`|
|NEAREST_GPS_CITY|`API_KEY`, `GPS_LAT`, `GPS_LON`|

```bash
docker build . -t tap:ingestion_manager
docker run -it --rm --hostname="ingestion_manager" --network tap tap:ingestion_manager
```

### Examples
- Get nearest city air quality data by GPS coordinates `docker run -it --rm --hostname="ingestion_manager" --network tap -e DATA_ACTION="NEAREST_GPS_CITY" tap:ingestion_manager`. It will work because ENV variables are already set in Dockerfile

- Get specified city air quality data `docker run -it --rm --hostname="ingestion_manager" --network tap -e DATA_ACTION="NEAREST_GPS_CITY" tap:ingestion_manager`

- Get all cities air quality data searching state name and country name `docker run -it --rm --hostname="ingestion_manager" --network tap -e DATA_ACTION="ALL_CITIES_BY_STATE_COUNTRY" -e COUNTRY_NAME="Italy" -e STATE_NAME="Campania" tap:ingestion_manager`

## Logstash
```bash
cd logstash
docker network create --subnet=10.0.100.0/24 tap
docker run --rm -it --hostname="logstash" -v $PWD/pipeline/from_python_to_kafka.conf:/usr/logstash/pipeline/logstash.conf --network tap -e XPACK_MONITORING_ENABLED=false docker.elastic.co/logstash/logstash:8.13.0
```

## Kafka
Get kafka:
```bash
wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
```

>Edit version if necessary [Versions](https://downloads.apache.org/kafka/)

---

#### [*EXTRA*] Lint with Pylint
```
cd python-ingestion
python3 -m pylint ingestion_manager.py
```
