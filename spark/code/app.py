from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline

kafkaServer = "kafkaServer:9092"
topic = "air-quality-monitor"
elastic_index = "aqm"
es_host = "elasticsearch:9200"

spark = SparkSession.builder \
    .appName("AirQualityPrediction") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoints") \
    .getOrCreate()

test_df = spark.createDataFrame([("test",)], ["message"])
test_df.write \
    .format("org.elasticsearch.spark.sql") \
    .option("es.resource", f"{elastic_index}") \
    .option("es.nodes", es_host) \
    .option("es.nodes.wan.only", "true") \
    .mode("append") \
    .save()

schema = StructType([
    StructField("wind_direction", DoubleType(), True),
    StructField("weather_timestamp", StringType(), True),
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
    StructField("@timestamp", StringType(), True),
    StructField("maincn", StringType(), True),
    StructField("pression", DoubleType(), True),
    StructField("pollution_timestamp", StringType(), True),
    StructField("aqius", IntegerType(), True),
    StructField("humidity", IntegerType(), True),
    StructField("@version", StringType(), True)
])

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafkaServer) \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .load()

df = df.selectExpr("CAST(value AS STRING) as json").select(from_json(col("json"), schema).alias("data")).select("data.*")

df = df.withColumn("weather_timestamp", to_timestamp(col("weather_timestamp")))
df = df.withColumn("pollution_timestamp", to_timestamp(col("pollution_timestamp")))

indexers = [StringIndexer(inputCol=column, outputCol=column+"_index") for column in ["state", "city", "tags", "country"]]
pipeline = Pipeline(stages=indexers)

feature_columns = ["wind_direction", "wind_speed", "temperature", "pression", "humidity", "state_index", "city_index", "tags_index", "country_index"]
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")

rf = RandomForestRegressor(featuresCol="features", labelCol="aqius")

def train_and_predict(batch_df, batch_id):
    if not batch_df.isEmpty():
        batch_df = pipeline.fit(batch_df).transform(batch_df)
        batch_df = assembler.transform(batch_df)
        
        # Suddivisione ei dati in training e test
        (trainingData, testData) = batch_df.randomSplit([0.8, 0.2])

        model = rf.fit(trainingData)

        predictions = model.transform(testData)
        evaluator = RegressionEvaluator(labelCol="aqius", predictionCol="prediction", metricName="rmse")
        rmse = evaluator.evaluate(predictions)
        print(f"Root Mean Squared Error (RMSE) on test data = {rmse}")

        streaming_predictions = model.transform(batch_df)
        
        output = streaming_predictions.select(
            col("weather_timestamp").alias("timestamp"),
            col("prediction").alias("predicted_aqius"),
            *feature_columns
        )
        
        output.show()

        output.write \
            .format("org.elasticsearch.spark.sql") \
            .option("es.resource", f"{elastic_index}") \
            .option("es.nodes", es_host) \
            .option("es.nodes.wan.only", "true") \
            .mode("append") \
            .save()

query = df.writeStream \
    .foreachBatch(train_and_predict) \
    .outputMode("append") \
    .start()

query.awaitTermination()
