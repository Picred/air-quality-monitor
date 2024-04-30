FROM docker.elastic.co/logstash/logstash:8.13.0

# Add your logstash plugins setup here
RUN logstash-plugin install logstash-filter-sentimentalizer 

# Build:
    # docker build . --tag tap:logstash
# Run:
    # docker run --rm -it --hostname="logstash" -v $PWD/pipeline/from_python_to_kafka.conf:/usr/logstash/pipeline/logstash.conf -e XPACK_MONITORING_ENABLED=false docker.elastic.co/logstash/logstash:8.13.0
# Codespaces: 
    # docker run --rm -it --hostname="logstash" -v ./pipeline/from_python_to_kafka.conf:/usr/logstash/pipeline/logstash.conf -e API_KEY=0e72cb61-87b6-4ab4-b422-0886e1305ac6 -e XPACK_MONITORING_ENABLED=false docker.elastic.co/logstash/logstash:8.13.0
