# Real-Time Air Quality Monitor

## Summary
- [Prerequisites](#prerequisites-)
- [Setup](#setup-)
    - [Apache Zookeeper, Apache Kafka, Logstash](#apache-zookeeper-apache-kafka-logstash)
    - [Docker Compose](#docker-compose)
    - [Useful links](#useful-links)
    - [Set Real-Time data with crontab](#set-real-time-data-with-crontab)
    - [Examples](#examples)
- [Getting new training data](#getting-new-training-data)
    - [Data Collection](#data-collection)
    - [Stopping new data collection](#stopping-new-data-collection)
    - [Update your model](#update-your-model)

## Prerequisites 📜
To use the Air-Quality Monitor app, you should have familiarity with the following technologies:
- [OpenWeather](https://home.openweathermap.org/users/sign_up) (*Register to obtain an API KEY*)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python](https://www.python.org/)
- [Crontab Docs](https://man7.org/linux/man-pages/man5/crontab.5.html)

## Setup ⚙️
To set up the Air Quality Monitor, follow these steps:

### Apache Zookeeper, Apache Kafka, Logstash
Download Kafka by running the following command:
```bash
cd kafka/setup
wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
cd ..
```
> *Edit the version if necessary [Versions](https://downloads.apache.org/kafka/)*

### Docker Compose
Run the following command to start the Docker Compose:
```bash
docker compose up --build
```

### Useful links:
- [Kafka UI](http://localhost:8080)
- [Spark UI](http://localhost:4040)
- [Elasticsearch UI](http://localhost:9200)
- [Kibana UI](http://localhost:5601)

## Set Real-Time data with crontab
After running *docker-compose*, the `ingestion_manager` container will complete its work in a few minutes. To generate additional data, you can set up an automatic job with **crontab** for other containers that handle the ingestion_manager.

- Open the crontab editor with `crontab -e`
- Add the following line to the crontab: `0 * * * * cd /full/path/air-quality-monitor && /usr/bin/docker compose up ingestion_manager >> /full/path/air-quality-monitor/cron.log 2>&1`
- Save the crontab file


### Start manual data ingestion
To start a **manually** real-time version of the app with real values, run the following command:
```bash
docker run -it --rm --hostname="ingestion_manager" --network aqm -e DATA_ACTION="NODEMO" air-quality-monitor-ingestion_manager
```

## Getting new training data 

### Data Collection every hour
1. **Start the Crontab (Linux)**: Add the following line to your crontab: `0 * * * * /full/path/air-quality-monitor/train.sh >> /full/path/air-quality-monitor/cron.log 2>&1`. This will schedule data collection every hour.
    - You can open the *crontab* editor with `crontab -e`
    - If you are not using Linux, you can start the script manually with `bash /full/path/air-quality-monitor/train.sh >> /full/path/air-quality-monitor/cron.log 2>&1`
    - **Note**: Ensure the Docker process has the correct permissions on the `./ingestion_manager/data` folder so it can insert new elements.
    - **Note**: Ensure to replace `/full/path/air-quality-monitor` with the correct path to the project folder.

2. **Uncomment the `historical_data` service** in the `docker-compose.yml` file.

3. **Build its image** with `docker compose build historical_data`.

4. **Wait for the scheduled time** for data collection to begin.

5. Check the log on `cron.log`
    - **Note**: Ensure the Docker process has the correct permissions on the `./ingestion_manager/data` folder so it can insert new elements.

6. **Model Evaluation**: After training, evaluate the model's performance to ensure it has improved with the addition of the new data.

### Stopping new data collection
- **Remove the Crontab Entry**: Remove the written line from your crontab 
- **Comment out the historical_data** service in the `docker-compose.yml` file.

### Update your model
1. **Uncomment the `train_model` service** in the `docker-compose.yml` file.

2. **Build its image** with `docker compose build train_model`.

3. **Start the container** with `docker compose up train_model`.

4. **Check** the model's files in `/spark/model`
