# Real-Time Air Quality Monitor

![AQM Dashboard](/media/aqm_dashboard.png)

## Summary 📑

- [Prerequisites](#prerequisites-)
- [Setup](#setup-️)
  - [Apache Zookeeper, Apache Kafka, Logstash](#apache-zookeeper-apache-kafka-logstash)
  - [Docker Compose](#docker-compose)
  - [Importing a Dashboard in Kibana (UI)](#importing-a-dashboard-in-kibana-ui)
  - [Useful links](#useful-links)
- [Set Real-Time data with crontab](#set-real-time-data-with-crontab)
  - [Start manual data ingestion](#start-manual-data-ingestion)
- [Getting new training data](#getting-new-training-data)
  - [Update your model](#update-your-model)
- [Screenshot](#screenshot)



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
wget https://downloads.apache.org/kafka/3.7.2/kafka_2.13-3.7.2.tgz
cd ..
```
> **Edit the version if necessary [Versions](https://downloads.apache.org/kafka/)**

```bash
template@version-edit:$~ wget https://downloads.apache.org/kafka/[NEW_VERSION]/kafka_[NEW_VERSION]
```

### Docker Compose
Run the following command to start the Docker Compose:
```bash
docker compose up --build
```

### Importing a Dashboard in Kibana (UI)
To import the dashboard on Kibana you must:
1. Open the left-side panel and click on **Stack Management**.
2. Navigate to **Saved Objects**.
3. Click **Import** (top-right corner) and select the file */kibana/kibana_dashboard.ndjson*


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
Just like the real-time data, you can also collect historical data to train your model.
- Check the following link to see the available data: [Historical Data](https://openweathermap.org/api/air-pollution)
- Generally use the API call: `http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={API key}`
- Save the historical data in the `data` folder with a name according to the `load()` function on the `save_old_data.py` file. Actually it is *milan_3months.json*

```python
with open('../data/milan_3munths.json') as f:
    data_raw = json.load(f)
```

- Run `python3 save_old_data.py`W

### Update your model
1. **Uncomment the `train_model` service** in the `docker-compose.yml` file.
2. **Build its image** with `docker compose build train_model`.
3. **Start the container** with `docker compose up train_model`.
4. **Check** the model's files in `/spark/model`

