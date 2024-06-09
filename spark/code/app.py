from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline, PipelineModel
import logging

# Configurazione del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurazione delle variabili
kafkaServer = "kafkaServer:9092"
topic = "air-quality-monitor"
elastic_index = "aqm"
es_host = "elasticsearch:9200"

# Creazione della sessione Spark
spark = SparkSession.builder \
    .appName("AirQualityMonitor") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoints") \
    .getOrCreate()

# Definizione dello schema per i dati in input
schema = StructType([
    StructField("wind_direction", DoubleType(), True),
    StructField("weather_timestamp", StringType(), True),
    StructField("state", StringType(), True),
    StructField("city", StringType(), True),
    StructField("gps_lat", DoubleType(), True),
    StructField("wind_speed", DoubleType(), True),
    StructField("country", StringType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("mainus", StringType(), True),
    StructField("aqicn", IntegerType(), True),
    StructField("icon", StringType(), True),
    StructField("gps_lon", DoubleType(), True),
    StructField("maincn", StringType(), True),
    StructField("pression", DoubleType(), True),
    StructField("pollution_timestamp", StringType(), True),
    StructField("aqius", IntegerType(), True),
    StructField("humidity", IntegerType(), True),
    StructField("@timestamp", StringType(), True)
])


# Lettura dei dati da Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafkaServer) \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .load()

# Conversione dei dati da formato Kafka
df = df.selectExpr("CAST(value AS STRING) as json").select(from_json(col("json"), schema).alias("data")).select("data.*")

model = PipelineModel.load("model")

predictions = model.transform(df).withColumnRenamed("prediction", "predicted_aqius")

selected_columns = ["city", "aqius", "predicted_aqius"]

selected_predictions = predictions.select(selected_columns)

# Conversione dei tipi di dati se necessario (esempio: conversione di interi in stringhe)
selected_predictions = selected_predictions.withColumn("aqius", col("aqius").cast("string"))
selected_predictions = selected_predictions.withColumn("prediction", col("predicted_aqius").cast("string"))

# Scrivi i dati selezionati e trasformati in Elasticsearch
selected_predictions.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .option("es.resource", f"{elastic_index}") \
    .option("es.nodes", es_host) \
    .option("es.nodes.wan.only", "true") \
    .start() \
    .awaitTermination()

# df.writeStream \
#     .format("org.elasticsearch.spark.sql") \
#     .option("es.resource", f"{elastic_index}") \
#     .option("es.nodes", es_host) \
#     .option("es.nodes.wan.only", "true") \
#     .start()\
#     .awaitTermination()
