FROM jupyter/pyspark-notebook:spark-3.1.1

# set python requirements for the container
RUN pip3 install pyspark kafka-utils numpy elasticsearch ipwhois pandas sklearn

WORKDIR /spark
ADD code/app.py .

ENTRYPOINT ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1", "--master", "local[4]", "app.py"]