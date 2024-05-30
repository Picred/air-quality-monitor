from pyspark import SparkContext # type: ignore
from pyspark.sql import SparkSession # type: ignore
from pyspark.streaming import StreamingContext # type: ignore
from pyspark.sql.dataframe import DataFrame #type: ignore

sc = SparkContext(appName="Air Quality Monitor")
spark = SparkSession(sc)
sc.setLogLevel("ERROR")

kafkaServer="kafkaServer:9092"
topic = "air-quality-monitor"

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", kafkaServer) \
  .option("subscribe", topic) \
  .option("startingOffsets", "earliest") \
  .load()

df=df.selectExpr("CAST(timestamp AS STRING)","CAST(value AS STRING)") # arriva un array di byte, non ho serializzato quindi devo farlo per forza.

df.writeStream \
  .format('console')\
  .option('truncate', 'false')\
  .start()\
  .awaitTermination()