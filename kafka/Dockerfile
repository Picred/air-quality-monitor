FROM amazoncorretto:17
LABEL maintainer="Salvo Nicotra"
ENV PATH /opt/kafka/bin:$PATH
ENV KAFKA_DIR "/opt/kafka"
ARG KAFKA_VERSION="2.13-3.7.0"

ADD setup/kafka_${KAFKA_VERSION}.tgz /opt

RUN ln -s /opt/kafka_${KAFKA_VERSION} ${KAFKA_DIR} 

ADD kafka-manager.sh ${KAFKA_DIR}/bin/kafka-manager
ADD conf/* ${KAFKA_DIR}/config/

USER root
RUN chmod 777 ${KAFKA_DIR}/bin/kafka-manager

ENTRYPOINT [ "kafka-manager" ]