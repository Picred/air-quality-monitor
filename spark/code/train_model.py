from pyspark.sql import SparkSession
from pyspark.sql.functions import when, from_json
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pyspark.sql.types import StructType, StructField, DoubleType

kafkaServer = "kafkaServer:9092"
topic = "air-quality-monitor"
elastic_index = "aqm"

spark = SparkSession.builder \
    .appName("LinearRegressionExample") \
    .getOrCreate()

df = spark \
  .read \
  .format("kafka") \
  .option("kafka.bootstrap.servers", kafkaServer) \
  .option("subscribe", topic) \
  .load()

schema = StructType([
    StructField("temperature", DoubleType(), True),
    StructField("humidity", DoubleType(), True),
    StructField("wind_speed", DoubleType(), True),
    StructField("pressure", DoubleType(), True),
    StructField("aqius", DoubleType(), True)
])

df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")

df = df.withColumn("non_empty", when(df.temperature.isNotNull(), 1).otherwise(0))

if df.filter(df.non_empty == 1).count() > 0:
    # Gestione dei valori nulli
    df = df.na.drop()  # Rimuovi le righe con valori nulli

    feature_columns = ["temperature", "humidity", "wind_speed", "pressure"]
    vector_assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")

    lr = LinearRegression(featuresCol="features", labelCol="aqius")  # Specifica la colonna target

    pipeline = Pipeline(stages=[vector_assembler, lr])

    model = pipeline.fit(df)
    
    predictions = model.transform(df)

    predictions.show()

else:
    print("Il dataset di addestramento è vuoto.")

spark.stop()
