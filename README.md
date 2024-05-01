# Real-Time Air Quality Monitor

# Prerequisites 📜
To use the Air-Flow Monitor, you should be familiar with the following:
- [Docker](https://www.docker.com/)
- [Python](https://www.python.org/)

# Setup ⚙️

## Kafka <img src="https://cdn.iconscout.com/icon/free/png-512/free-kafka-282292.png?f=webp&w=256" alt="Kafka Image" width="30">
Get kafka:
```bash
cd kafka/setup
wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
cd ..
```
> *Edit version if necessary [Versions](https://downloads.apache.org/kafka/)*

### Automatically <img src="https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/97_Docker_logo_logos-256.png" alt="Kafka UI Image" width="50">

Create Zookeeper, Kafka Server and Kafka UI containers:
```bash
cd kafka
docker-compose up
```

### Manually
Move on kafka directory, then:

#### 1. Zookeper <img src="https://cdn.icon-icons.com/icons2/2699/PNG/512/apache_zookeeper_logo_icon_169571.png" alt="Zookeeper Image" width="50">
```bash
docker build . --tag tap:kafka
docker run -e KAFKA_ACTION=start-zk --network tap --ip 10.0.100.22  -p 2181:2181 --name kafkaZK --rm -it tap:kafka
docker start kafkaZK
```
#### 2. Kafka Server & Kafka UI <img src="https://d7umqicpi7263.cloudfront.net/img/product/5bf37906-9e7a-4dd4-97a7-45b680b46833.com/2d35d7ca04a996133f35c99d2d6ac2c9" alt="Kafka UI Image" width="50">
```bash
docker run -e KAFKA_ACTION=start-kafka --network tap --ip 10.0.100.23 -p 9092:9092 --name kafkaServer --rm -it tap:kafka
```
```bash
docker run --network tap -e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=10.0.100.23:9092 -e KAFKA_CLUSTERS_0_ZOOKEEPER=10.0.100.22:2181 -p 8080:8080 --name KafkaUI --rm provectuslabs/kafka-ui:latest
```

> http://localhost:8080 to see KafkaUI



## Ingestion Manager <img src="https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/267_Python_logo-256.png" alt="Python Image" width="30">

To execute the script within the container, environment variables must be set. Specifically, variables need to be configured based on the desired data collection:

`API_KEY` = Your [IQAIR](https://www.iqair.com) API key  
`DATA_ACTION =  ["ALL_COUNTRIES" | "ALL_STATES_BY_COUNTRY" | "ALL_CITIES_BY_STATECOUNTRY" | "NEAREST_IP_CITY" | "NEAREST_GPS_CITY"]`. Default value is `NEAREST_IP_CITY`


Below are the environment variables to be set according to the `DATA_ACTION`:
|DATA_ACTION|Dependencies|
|---|---|
|ALL_COUNTRIES|API_KEY|
|NEAREST_IP_CITY|API_KEY|
|ALL_STATES_BY_COUNTRY|API_KEY, STATE_NAME|
|ALL_CITIES_BY_STATE_COUNTRY|API_KEY, STATE_NAME, COUNTRY_NAME|
|NEAREST_GPS_CITY|API_KEY, GPS_LAT, GPS_LON|

```bash
cd python-ingestion
docker build . -t tap:ingestion_manager
docker run -it --rm --hostname="ingestion_manager" --network tap tap:ingestion_manager
```

### Examples
- Get nearest city air quality data by GPS coordinates `docker run -it --rm --hostname="ingestion_manager" --network tap -e DATA_ACTION="NEAREST_GPS_CITY" tap:ingestion_manager`. It will work because ENV variables are already set in Dockerfile

- Get specified city air quality data `docker run -it --rm --hostname="ingestion_manager" --network tap -e DATA_ACTION="NEAREST_GPS_CITY" tap:ingestion_manager`

- Get all cities air quality data searching state name and country name `docker run -it --rm --hostname="ingestion_manager" --network tap -e DATA_ACTION="ALL_CITIES_BY_STATE_COUNTRY" -e COUNTRY_NAME="Italy" -e STATE_NAME="Campania" tap:ingestion_manager`

## Logstash <img src="https://cdn.iconscout.com/icon/free/png-512/free-logstash-3521553-2944971.png?f=webp&w=256" alt="Logstash Image" width="30">

```bash
cd logstash
docker network create --subnet=10.0.100.0/24 tap
docker run --rm -it --hostname="logstash" -v $PWD/pipeline/from_python_to_kafka.conf:/usr/share/logstash/pipeline/logstash.conf --network tap -e XPACK_MONITORING_ENABLED=false docker.elastic.co/logstash/logstash:8.13.0
cd ..
```

## Add Topic
```bash
docker run -e KAFKA_ACTION=create-topic -e KAKFA_SERVER=10.0.100.23 -e KAFKA_TOPIC=air-quality-monitor --network tap --ip 10.0.100.24 --rm --name kafkaTopic -it tap:kafka
```



---

#### [*EXTRA*] Lint with Pylint
```bash
cd python-ingestion
python3 -m pylint ingestion_manager.py
```

- Test Console Consumer
    ```bash
    docker run -e KAFKA_ACTION=consumer -e KAFKA_TOPIC=air-quality-monitor --network tap -it tap:kafka
    ```