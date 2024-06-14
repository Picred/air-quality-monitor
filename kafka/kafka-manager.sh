#!/bin/bash
ZK_DATA_DIR=/tmp/zookeeper
ZK_SERVER="localhost"
EXTRA_KAFKA_GROUP_ID=""

[[ -z "${KAFKA_ACTION}" ]] && { echo "KAFKA_ACTION required"; exit 1; }
[[ -z "${KAFKA_DIR}" ]] && { echo "KAFKA_DIR missing"; exit 1; }
[[ -z "${KAFKA_CONFIG}" ]] && { KAFKA_CONFIG="server.properties"; }
[[ -z "${KAFKA_PARTITION}" ]] && { KAFKA_PARTITION=1; }
[[ "${KAFKA_GROUP_ID}" ]] && { EXTRA_KAFKA_GROUP_ID="--consumer-property group.id=${KAFKA_GROUP_ID}"; } 

case ${KAFKA_ACTION} in
    "start-zk")
    echo "Starting ZK"
    mkdir -p ${ZK_DATA_DIR}; # Data dir is setup in conf/zookeeper.properties
    zookeeper-server-start.sh ${KAFKA_DIR}/config/zookeeper.properties
    ;;
    "start-kafka")
    kafka-server-start.sh ${KAFKA_DIR}/config/${KAFKA_CONFIG}
esac