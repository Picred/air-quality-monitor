from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql.dataframe import DataFrame

sc = SparkContext(appName="AQM_test")
spark = SparkSession(sc)
sc.setLogLevel("ERROR")

kafkaServer="kafkaServer:9092"
topic = "air-quality-monitor"

# Streaming Query

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", kafkaServer) \
  .option("subscribe", topic) \
  .load()

# Arricchimento. Successivamente aggiungeremo una Transform, cioè verranno aggiunte delle colonne
df=df.selectExpr("CAST(timestamp AS STRING)","CAST(value AS STRING)") # arriva un array di byte, non ho serializzato quindi devo farlo per forza.

# Scrivo su console. Sarà in formato ES successivamente
df.writeStream \
  .format('console')\
  .option('truncate', 'false')\
  .start()\
  .awaitTermination()