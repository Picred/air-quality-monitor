from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType, TimestampType
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline, PipelineModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

kafkaServer = "kafkaServer:9092"
topic = "air-quality-monitor"
elastic_index = "aqm"
es_host = "elasticsearch:9200"

# Creazione della sessione Spark
spark = SparkSession.builder \
    .appName("AirQualityMonitor") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoints") \
    .getOrCreate()

schema = StructType([
    StructField("aqi", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("co", FloatType(), True),
    StructField("lat", FloatType(), True),
    StructField("lon", FloatType(), True),
    StructField("nh3", FloatType(), True),
    StructField("no", FloatType(), True),
    StructField("no2", FloatType(), True),
    StructField("pm10", FloatType(), True),
    StructField("pm2_5", FloatType(), True),
    StructField("so2", FloatType(), True),
    StructField("timestamp_utc", StringType(), True)
])

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafkaServer) \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .load()

df = df.selectExpr("CAST(value AS STRING) as json").select(from_json(col("json"), schema).alias("data")).select("data.*")

model = PipelineModel.load("model")

predictions = model.transform(df).withColumnRenamed("prediction", "predicted_aqi")

selected_columns = ["city", "aqi", "predicted_aqi"]

selected_predictions = predictions.select(selected_columns)

selected_predictions = selected_predictions.withColumn("aqi", col("aqi").cast("string"))
selected_predictions = selected_predictions.withColumn("prediction", col("predicted_aqi").cast("string"))

selected_predictions.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .option("es.resource", f"{elastic_index}") \
    .option("es.nodes", es_host) \
    .option("es.nodes.wan.only", "true") \
    .start() \
    .awaitTermination()
