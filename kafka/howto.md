# Start Kafka

#### Bisogna scaricare kafka.tgz -> `wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz` e metterlo in `setup/`

#### Settare il Dockerfile
```Dockerfile
FROM amazoncorretto:17
LABEL maintainer="Andrei Daniel Stefan"
ENV PATH /opt/kafka/bin:$PATH
ENV KAFKA_DIR "/opt/kafka"
ARG KAFKA_VERSION="2.13-3.7.0"

# Installing Kafka
# ADD will automatically extract the file
ADD setup/kafka_${KAFKA_VERSION}.tgz /opt

# Create Sym Link 
RUN ln -s /opt/kafka_${KAFKA_VERSION} ${KAFKA_DIR} 

ADD kafka-manager.sh ${KAFKA_DIR}/bin/kafka-manager
# Copy All conf here
ADD conf/* ${KAFKA_DIR}/config/

# Edit perms to run entrypoint
USER root
RUN chmod 777 ${KAFKA_DIR}/bin/kafka-manager

ENTRYPOINT [ "kafka-manager" ]
```

#### Far partire Zookeeper
```bash
docker stop kafkaZK
docker container rm kafkaZK
docker build . --tag tap:kafka
docker run -e KAFKA_ACTION=start-zk --network tap --ip 10.0.100.22  -p 2181:2181 --name kafkaZK --rm -it tap:kafka
docker start kafkaZK
```

#### Kafka Server
Dopo aver fatto partire ZK, si deve configurare il file `kafka/conf/server.properties` e settare `zookeeper.connect=kafkaZk:2181` in modo tale da sapere a quale ZK si deve attaccare il Kafka Server.

```bash
docker stop kafkaServer
docker container rm kafkaServer
docker build . --tag tap:kafka
docker run -e KAFKA_ACTION=start-kafka --network tap --ip 10.0.100.23 -p 9092:9092 --name kafkaServer --rm -it tap:kafka
```

### Kafka UI
```bash
docker run --network tap -e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=10.0.100.23:9092 -e KAFKA_CLUSTERS_0_ZOOKEEPER=10.0.100.22:2181 -p 8080:8080 --name KafkaUI --rm provectuslabs/kafka-ui:latest
```

UI: http://localhost:8080/

### Add Topic
```bash
docker stop kafkaTopic
docker container rm kafkaTopic
docker build . --tag tap:kafka
docker run -e KAFKA_ACTION=create-topic -e KAKFA_SERVER=10.0.100.23 -e KAFKA_TOPIC=air-quality-monitor --network tap --ip 10.0.100.24 --rm --name kafkaTopic -it tap:kafka
```
Il container si stoppa e viene aggiunto un Topic. Si può vedere il Topic dall'UI.

<!-- ### Add Producer
Aggiungo un Producer
```bash
docker build . --tag tap:kafka
docker run -e KAFKA_ACTION=producer -e KAFKA_TOPIC=air-quality-monitor --network tap -it tap:kafka
```


### Add Consumer
```bash
docker build . --tag tap:kafka
docker run -e KAFKA_ACTION=consumer -e KAFKA_TOPIC=air-quality-monitor --network tap -it tap:kafka
```


```bash
docker build . -t tap:logstash
docker run --rm -p 8181:8181 -it --name "logstash" --hostname="logstash" -v ./pipeline/nearest_city.conf:/usr/share/logstash/pipeline/logstash.conf -e XPACK_MONITORING_ENABLED=false --network tap tap:logstash
``` -->

Ora sul Consumer di Kafka dovrei avere qualcosa tipo: *timestamp %host: %message*