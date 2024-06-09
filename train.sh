#!/bin/bash

echo "Starting ingestion manager"

# while true
# do
/usr/bin/docker run --rm --hostname="ingestion_manager" --network aqm -e DATA_ACTION="NODEMO" -v /home/andrei/air-quality-monitor/ingestion_manager/data:/ingestion_manager/data air-quality-monitor-ingestion_manager
#     sleep 10
# done