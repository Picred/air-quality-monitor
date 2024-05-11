# Real-Time Air Quality Monitor

# Prerequisites 📜
To use the Air-Flow Monitor app, you should be familiar with the following:
- [IQAir](https://www.iqair.com) *Register to obtain API KEY*
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python](https://www.python.org/)

# Setup ⚙️

## Apache Zookeeper, Apache Kafka <img src="https://cdn.iconscout.com/icon/free/png-512/free-kafka-282292.png?f=webp&w=256" alt="Kafka Image" width="30">, Logstash <img src="https://cdn.iconscout.com/icon/free/png-512/free-logstash-3521553-2944971.png?f=webp&w=256" alt="Logstash Image" width="30">


Get kafka:
```bash
cd kafka/setup
wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
cd ..
```
> *Edit version if necessary [Versions](https://downloads.apache.org/kafka/)*

### Docker Compose<img src="https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/97_Docker_logo_logos-256.png" alt="Kafka UI Image" width="50">

Create Zookeeper, Kafka Server, Kafka UI, Logstash and Ingestion Manager containers:
```bash
docker-compose up
```

> http://localhost:8080 to see KafkaUI


# How to get data (*Ingestion Manager Container*) <img src="https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/267_Python_logo-256.png" alt="Python Image" width="30">

After running *docker-compose*, you can generate additional data by starting other containers that handle the ingestion_manager. Just configure properly environment variables:

```bash
API_KEY = 123abc # Your IQAir API key  
DATA_ACTION = [ "ALL_COUNTRIES" | "ALL_STATES_BY_COUNTRY" | "ALL_CITIES_BY_STATECOUNTRY" | "NEAREST_IP_CITY" | "NEAREST_GPS_CITY"] # Default value is NEAREST_GPS_CITY
```


Below are the environment variables to be set according to the `DATA_ACTION`:
|           DATA_ACTION          |                    DEPENDENCIES               |
|:------------------------------:|:---------------------------------------------:|
|          ALL_COUNTRIES         |                      API_KEY                  |
|         NEAREST_IP_CITY        |                      API_KEY                  |
|       ALL_STATES_BY_COUNTRY    |                 API_KEY, STATE_NAME           |
|   ALL_CITIES_BY_STATE_COUNTRY  |         API_KEY, STATE_NAME, COUNTRY_NAME     |
|        NEAREST_GPS_CITY        |           API_KEY, GPS_LAT, GPS_LON           |
|         SPECIFIC_CITY          |API_KEY, STATE_NAME, COUNTRY_NAME, CITY_TO_SCAN|


### Examples

```bash
# Get nearest city air quality data by IP address
docker run -it --rm --hostname="ingestion_manager" --network aqm -e DATA_ACTION="NEAREST_IP_CITY" air-quality-monitor-ingestion_manager`. 
```

*It will works because **ENV variables** are already set in `docker-compose.yaml` file.*

```bash
# Get specified city air quality data:
docker run -it --rm --hostname="ingestion_manager" --network aqm -e DATA_ACTION="SPECIFIC_CITY" -e COUNTRY_NAME="Italy" -e STATE_NAME="Campania" -e CITY_TO_SCAN="Naples" air-quality-monitor-ingestion_manager
```

```bash
# Get all available cities searching by state name and country name:
docker run -it --rm --hostname="ingestion_manager" --network aqm -e DATA_ACTION="ALL_CITIES_BY_STATE_COUNTRY" -e COUNTRY_NAME="Italy" -e STATE_NAME="Campania" air-quality-monitor-ingestion_manager
```


## Spark

<!--  TODO -->

---