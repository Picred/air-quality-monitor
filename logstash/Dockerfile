FROM docker.elastic.co/logstash/logstash:8.13.0

WORKDIR /app
# Add your logstash plugins setup here
COPY ingestion_manager.py .
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-pip

RUN pip install -r requirements.txt
RUN python3 ingestion_manager.py
# RUN logstash-plugin install logstash-filter-sentimentalizer 

# to build with
# docker build . --tag tap:logstash
# and run with
# docker run --rm -it --hostname="logstash" -v $PWD/pipeline/from_python_to_kafka.conf:/usr/logstash/pipeline/logstash.conf -e XPACK_MONITORING_ENABLED=false docker.elastic.co/logstash/logstash:8.13.0
# Codespaces: docker run --rm -it --hostname="logstash" -v ./pipeline/from_python_to_kafka.conf:/usr/logstash/pipeline/logstash.conf -e API_KEY=0e72cb61-87b6-4ab4-b422-0886e1305ac6 -e XPACK_MONITORING_ENABLED=false docker.elastic.co/logstash/logstash:8.13.0
