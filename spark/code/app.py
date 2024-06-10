from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType
from pyspark.ml import PipelineModel
import logging

def create_spark_session() -> SparkSession:
    """
    Create a SparkSession object.

    Returns:
        SparkSession: The created SparkSession object.
    """
    return SparkSession.builder \
        .appName("AirQualityMonitor") \
        .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoints") \
        .getOrCreate()

def load_data(spark: SparkSession, kafka_server: str, topic: str) -> DataFrame:
    """
    Load data from Kafka into a DataFrame.

    Args:
        spark (SparkSession): The SparkSession object.
        kafka_server (str): The Kafka server address.
        topic (str): The Kafka topic to subscribe to.

    Returns:
        DataFrame: The loaded DataFrame.
    """
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_server) \
        .option("subscribe", topic) \
        .option("startingOffsets", "earliest") \
        .load()

    return df.selectExpr("CAST(value AS STRING) as json").select(from_json(col("json"), schema).alias("data")).select("data.*")

def transform_data(df: DataFrame, model: PipelineModel) -> DataFrame:
    """
    Transform the data using a trained model.

    Args:
        df (DataFrame): The input DataFrame.
        model (PipelineModel): The trained model.

    Returns:
        DataFrame: The transformed DataFrame.
    """
    predictions = model.transform(df).withColumnRenamed("prediction", "predicted_aqi")
    
    selected_columns = ["city", "aqi", "predicted_aqi", "timestamp_utc", "@timestamp", "lat", "lon", "co", "nh3", "no", "no2", "pm10", "pm2_5", "so2"]
    selected_predictions = predictions.select(selected_columns)
    return selected_predictions

def write_to_elasticsearch(df: DataFrame, elastic_index: str, es_host: str) -> None:
    """
    Write the DataFrame to Elasticsearch.

    Args:
        df (DataFrame): The DataFrame to write.
        elastic_index (str): The Elasticsearch index.
        es_host (str): The Elasticsearch host.

    Returns:
        None
    """
    df.writeStream \
        .format("org.elasticsearch.spark.sql") \
        .option("es.resource", f"{elastic_index}") \
        .option("es.nodes", es_host) \
        .option("es.nodes.wan.only", "true") \
        .start() \
        .awaitTermination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    kafka_server = "kafkaServer:9092"
    topic = "air-quality-monitor"
    elastic_index = "aqm"
    es_host = "http://elasticsearch:9200"

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
        StructField("timestamp_utc", StringType(), True),
        StructField("@timestamp", StringType(), True)
    ])

    spark = create_spark_session()
    df = load_data(spark, kafka_server, topic)
    model = PipelineModel.load("model")
    transformed_df = transform_data(df, model)
    write_to_elasticsearch(transformed_df, elastic_index, es_host)
