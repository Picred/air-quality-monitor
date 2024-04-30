# Real-time air quality tracking software


# Prerequisites
To use the Air-Flow Monitor, you should be familiar with the following:
- [Docker](https://www.docker.com/)
- [Python](https://www.python.org/)

# Setup

## Python Ingestion Manager
To execute the script within the container, environment variables must be set. Specifically, variables need to be configured based on the desired data collection:

`API_KEY` = Your [IQAIR](https://www.iqair.com) API key  
`DATA_ACTION =  ["ALL_COUNTRIES" | "ALL_STATES_BY_COUNTRY" | "ALL_CITIES_BY_STATECOUNTRY" | "NEAREST_IP_CITY" | "NEAREST_GPS_CITY"]`. Default value is `NEAREST_IP_CITY`


Below are the environment variables to be set according to the `DATA_ACTION`:
`ALL_COUNTRIES` -> `API_KEY`
`ALL_STATES_BY_COUNTRY` -> `API_KEY`, `STATE_NAME`
`ALL_CITIES_BY_STATE_COUNTRY` -> `API_KEY`,  `STATE_NAME`, `COUNTRY_NAME`
`NEAREST_IP_CITY` -> `API_KEY`
`NEAREST_GPS_CITY` -> `API_KEY`, `GPS_LAT`, `GPS_LON`"


## Logstash
```bash
cd logstash
docker network create --subnet=10.0.100.0/24 tap
docker build . --tag tap:logstash
docker run --rm -it --hostname="logstash" -v $PWD/pipeline/httpoller.conf:/usr/share/logstash/pipeline/logstash.conf -e XPACK_MONITORING_ENABLED=false docker.elastic.co/logstash/logstash:8.13.0
```

## Kafka
Get kafka:
```bash
wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
```

>Edit version if necessary [Versions](https://downloads.apache.org/kafka/)