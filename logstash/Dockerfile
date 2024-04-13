FROM docker.elastic.co/logstash/logstash:8.13.0

# Add your logstash plugins setup here
RUN logstash-plugin install logstash-filter-sentimentalizer 

# to build with
# docker build . --tag tap:logstash
# and run with
# docker run --rm -it --hostname="logstash" -v $PWD/pipeline/httpoller.conf:/usr/logstash/pipeline/logstash.conf -e XPACK_MONITORING_ENABLED=false docker.elastic.co/logstash/logstash:8.13.0
# make sure that pipeline dir with proper conf is there%
