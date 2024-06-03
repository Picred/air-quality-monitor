from pyspark import SparkContext # type: ignore
from pyspark.sql import SparkSession # type: ignore
from pyspark.streaming import StreamingContext # type: ignore
from pyspark.sql.dataframe import DataFrame #type: ignore
# from elasticsearch import Elasticsearch
# elastic = Elasticsearch(hosts=["http://elasticsearch:9200"])
# mapping = {
#     "mappings": {
#         "properties": {
#             "timestamp": {
#                 "type": "date"
#             }
#         }
#     }
# }
# elastic_index = "aqm"
# # make an API call to the Elasticsearch cluster
# # and have it return a response:
# response = elastic.indices.create(
#     index=elastic_index,
#     body=mapping,
#     ignore=400 # ignore 400 already exists code
# )
# if 'acknowledged' in response:
#     if response['acknowledged'] == True:
#         print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])
#     # catch API error response
#     elif 'error' in response:
#         print ("ERROR:", response['error']['root_cause'])
#         print ("TYPE:", response['error']['type'])
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
# # Configurazione di Elasticsearch
# es_host = "http://elasticsearch:9200"  # Modifica se necessario
# es_index = "air-quality-monitor"

df.writeStream \
  .format('console')\
  .option('truncate', 'false')\
  .start()\
  .awaitTermination()

# # Scrittura dello stream su Elasticsearch
# df.writeStream \
#     .format("org.elasticsearch.spark.sql") \
#     .option("checkpointLocation", "/path/to/checkpoint/dir") \
#     .option("es.nodes", es_host) \
#     .option("es.resource", es_index) \
#     .start() \
#     .awaitTermination()