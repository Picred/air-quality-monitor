from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline
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
    StructField("weather_timestamp", StringType(), True), # TimestampType()
    StructField("state", StringType(), True),
    StructField("city", StringType(), True),
    StructField("gps_lat", DoubleType(), True),
    StructField("wind_speed", DoubleType(), True),
    StructField("tags", StringType(), True),
    StructField("country", StringType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("mainus", StringType(), True),
    StructField("aqicn", IntegerType(), True),
    StructField("icon", StringType(), True),
    StructField("gps_lon", DoubleType(), True),
    StructField("maincn", StringType(), True),
    StructField("pression", DoubleType(), True),
    StructField("pollution_timestamp", StringType(), True), # TimestampType()
    StructField("aqius", IntegerType(), True),
    StructField("humidity", IntegerType(), True),
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

# Preprocessing dei dati
df = df.withColumn("weather_timestamp", to_timestamp(col("weather_timestamp")))
df = df.withColumn("pollution_timestamp", to_timestamp(col("pollution_timestamp")))

# Codifica delle variabili categoriche
indexers = [StringIndexer(inputCol=column, outputCol=column+"_index") for column in ["state", "city", "country"]]
pipeline = Pipeline(stages=indexers)

# Selezione delle caratteristiche
feature_columns = ["wind_direction", "wind_speed", "temperature", "pression", "humidity", "state_index", "city_index", "country_index"]
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")

# Modello di regressione
lr = LinearRegression(featuresCol="features", labelCol="aqius")

# Funzione di aggiornamento del modello
def train_and_predict(batch_df, batch_id):
    if not batch_df.isEmpty():
        logger.info("Processing batch id: %d", batch_id)
        logger.info("Batch data schema:")
        batch_df.printSchema()
        logger.info("Batch data preview:")
        batch_df.show(truncate=False)
        try:
            # Preprocessing dei dati nel batch
            batch_df = pipeline.fit(batch_df).transform(batch_df)
            batch_df = assembler.transform(batch_df)
            
            # Suddivisione dei dati in training e test
            (trainingData, testData) = batch_df.randomSplit([0.8, 0.2])

            # Addestramento del modello
            model = lr.fit(trainingData)

            # Predizione e valutazione
            predictions = model.transform(testData)
            evaluator = RegressionEvaluator(labelCol="aqius", predictionCol="prediction", metricName="rmse")
            rmse = evaluator.evaluate(predictions)
            logger.info(f"Root Mean Squared Error (RMSE) on test data = {rmse}")
            # Esegui previsioni sui dati in streaming
            streaming_predictions = model.transform(batch_df)
            
            # Preparazione dei dati per Elasticsearch
            output = streaming_predictions.select(
                col("weather_timestamp").alias("timestamp"),
                col("prediction").alias("predicted_aqius"),
                *feature_columns,
                "weather_timestamp",
                "state",
                "city",
                "gps_lat",
                "country",
                "mainus",
                "aqicn",
                "icon",
                "gps_lon",
                "maincn",
                "pollution_timestamp",
                "aqius",
            )
            
            # Log dei dati prima di scriverli su Elasticsearch
            print("Data before writing to Elasticsearch:")
            output.show(truncate=False)

            # Controlla lo schema del DataFrame output
            output.printSchema()

            # Scrittura dei dati su Elasticsearch
            output.write \
                .format("org.elasticsearch.spark.sql") \
                .option("es.resource", f"{elastic_index}") \
                .option("es.nodes", es_host) \
                .option("es.nodes.wan.only", "true") \
                .mode("append") \
                .save()
        except Exception as e:
            print("An error occurred:", str(e))
            logger.error("An error occurred during batch processing: %s", e)
    else:
        logger.info("No data received in batch id: %d", batch_id)

# Esecuzione del modello di machine learning sui dati in streaming
query = df.writeStream \
    .foreachBatch(train_and_predict) \
    .outputMode("append") \
    .start()

query.awaitTermination()
