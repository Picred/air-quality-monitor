# air-flow-monitor
Real-time air quality tracking software

# Prerequisites
To use the Air-Flow Monitor, you should be familiar with the following:
- [Docker](https://www.docker.com/)
- [Python](https://www.python.org/)
- API key (dipende dal provider scelto)


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