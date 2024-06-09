from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pyspark.ml.pipeline import PipelineModel


def create_spark_session() -> SparkSession:
    """
    Create a SparkSession object.
    
    Returns:
        SparkSession: The SparkSession object.
    """
    spark = SparkSession.builder \
        .appName("AQM - Model Training") \
        .getOrCreate()
    return spark

def load_dataset(spark: SparkSession, file_path: str) -> DataFrame:
    """
    Load the dataset from a CSV file.
    
    Args:
        spark (SparkSession): The SparkSession object.
        file_path (str): The path to the CSV file.
    
    Returns:
        DataFrame: The loaded dataset.
    """
    schema = StructType([
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("country", StringType(), True),
        StructField("gps_lat", FloatType(), True),
        StructField("gps_lon", FloatType(), True),
        StructField("pollution_timestamp", StringType(), True),
        StructField("aqius", IntegerType(), True),
        StructField("mainus", StringType(), True),
        StructField("aqicn", IntegerType(), True),
        StructField("maincn", StringType(), True),
        StructField("weather_timestamp", StringType(), True),
        StructField("temperature", FloatType(), True),
        StructField("pression", FloatType(), True),
        StructField("humidity", FloatType(), True),
        StructField("wind_speed", FloatType(), True),
        StructField("wind_direction", FloatType(), True),
    ])
    dataset = spark.read.format("csv") \
        .option("header", "true") \
        .schema(schema) \
        .load(file_path)
    return dataset

def train_linear_regression_model(dataset: DataFrame) -> PipelineModel:
    """
    Train a linear regression model using the dataset.
    
    Args:
        dataset (DataFrame): The dataset to train the model on.
    
    Returns:
        PipelineModel: The trained linear regression model.
    """
    feature_columns = ["temperature", "pression", "humidity", "wind_speed", "wind_direction"]
    assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
    lr = LinearRegression(featuresCol="features", labelCol="aqius")
    pipeline = Pipeline(stages=[assembler, lr])
    train_data, test_data = dataset.randomSplit([0.8, 0.2], seed=12345)
    model = pipeline.fit(train_data)
    return model

def evaluate_model(model: PipelineModel, test_data: DataFrame) -> None:
    """
    Evaluate the trained model.
    
    Args:
        model (PipelineModel): The trained model.
        test_data (DataFrame): The test dataset.
    """
    predictions = model.transform(test_data)
    predictions.select("city", "aqius", "prediction").show()
    training_summary = model.stages[-1].summary
    print("RMSE: %f" % training_summary.rootMeanSquaredError)
    print("r2: %f" % training_summary.r2)

def save_model(model: PipelineModel, file_path: str) -> None:
    """
    Save the trained model to a file.
    
    Args:
        model (PipelineModel): The trained model.
        file_path (str): The path to save the model.
    """
    model.write().overwrite().save(file_path)

def stop_spark_session(spark: SparkSession) -> None:
    """
    Stop the SparkSession.
    
    Args:
        spark (SparkSession): The SparkSession object.
    """
    spark.stop()


if __name__ == "__main__":
    spark = create_spark_session()
    dataset = load_dataset(spark, "data.csv")
    train_data, test_data = dataset.randomSplit([0.8, 0.2], seed=12345)
    model = train_linear_regression_model(train_data)
    evaluate_model(model, test_data)
    save_model(model, "model")
    stop_spark_session(spark)
