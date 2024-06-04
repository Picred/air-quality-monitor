from pyspark import SparkContext # type: ignore
from pyspark.sql import SparkSession # type: ignore
from pyspark.streaming import StreamingContext # type: ignore
from pyspark.sql.dataframe import DataFrame #type: ignore
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
import pyspark.sql.types as tp
from pyspark.sql.functions import from_json

# sc = SparkContext(appName="Air Quality Monitor")
# spark = SparkSession(sc)
# sc.setLogLevel("ERROR")
#  ------------------------------------------------------
kafkaServer="kafkaServer:9092"
topic = "air-quality-monitor"
elastic_index="aqm"

sparkConf = SparkConf().set("es.nodes", "elasticsearch") \
                        .set("es.port", "9200")

spark = SparkSession.builder.appName("Air Quality Monitor").config(conf=sparkConf).getOrCreate()
# To reduce verbose output
spark.sparkContext.setLogLevel("ERROR") 


df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", kafkaServer) \
  .option("subscribe", topic) \
  .option("startingOffsets", "earliest") \
  .load()


aqm_data = tp.StructType([
    tp.StructField(name= 'city',       dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'state',      dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'country',    dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'location',   dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'pollution',  dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'weather',    dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'gps_lat',    dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'gps_lon',    dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'pollution_timestamp', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'aqius',      dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'mainus',     dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'aqicn',      dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'maincn',     dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'weather_timestamp', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'temperature',dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'pression',   dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'humidity',   dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'wind_speed', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'wind_direction', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'icon',       dataType= tp.StringType(),  nullable= True)

    
    
])

df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", aqm_data).alias("data")) \

df = df.select("data")
# df=df.selectExpr("CAST(timestamp AS STRING)","CAST(value AS STRING)") # arriva un array di byte, non ho serializzato quindi devo farlo per forza.
# # Configurazione di Elasticsearch
es_host = "http://elasticsearch:9200"  # Modifica se necessario

df.writeStream \
  .format('console')\
  .option('truncate', 'false')\
  .start()\
  .awaitTermination()

# df.writeStream \
#    .option("checkpointLocation", "/tmp/") \
#    .format("es") \
#    .start(elastic_index) \
#    .awaitTermination()

# # Scrittura dello stream su Elasticsearch
# df.writeStream \
#     .format("org.elasticsearch.spark.sql") \
#     .option("checkpointLocation", "/tmp/") \
#     .option("es.nodes", es_host) \
#     .option("es.resource", elastic_index) \
#     .start() \
#     .awaitTermination()
