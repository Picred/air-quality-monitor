FROM apache/spark:python3

USER root

WORKDIR /app
RUN pip3 install pyspark kafka-utils folium
COPY app.py .

# Copia il file di configurazione di Spark (se necessario)
# COPY spark-defaults.conf /opt/spark/conf/spark-defaults.conf

# Imposta le variabili d'ambiente per Spark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Comando di avvio predefinito
# CMD ["/opt/spark/bin/pyspark"]
CMD ["python3", "app.py"]

# docker build -t spark-pyspark . && docker run -it spark-pyspark -v .:/app