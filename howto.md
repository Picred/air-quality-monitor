Rivediamo: https://github.com/tapunict/tap2024/blob/main/doc/Spark%20Structured%20Streaming.ipynb

il foreach() dà un output

Per scrivere su file (traint model) si usa:
```python
writeStream
    .format("parquet")        // can be "orc", "json", "csv", etc.
    .option("path", "path/to/destination/dir")
    .start()
```

`transform()` è un arricchimento che aggiunge una colonna.

Con il foreach() si usa un altro tipo di sink che non è più streaming. In questo caso si usa quando si comunica con un sink esterno. Esso può anche non essere fatto in modo ordinato.

Invece foreachBatch() è consigliato perchè lavora in Streaming.

***Entrambi i foreach() si usano per richiamare API esterne, quindi in questo caso non mi serve per forza, visto che non si possono sincronizzare con lo streaming***. Si usa anche per scrivere su sink differenti.


# Linear Regression
https://spark.apache.org/docs/latest/ml-classification-regression.html#linear-regression

```python
from pyspark.ml.regression import LinearRegression

# Load training data
training = spark.read.format("libsvm")\
    .load("data/mllib/sample_linear_regression_data.txt")

lr = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

# Fit the model
lrModel = lr.fit(training)

# Print the coefficients and intercept for linear regression
print("Coefficients: %s" % str(lrModel.coefficients))
print("Intercept: %s" % str(lrModel.intercept))

# Summarize the model over the training set and print out some metrics
trainingSummary = lrModel.summary
print("numIterations: %d" % trainingSummary.totalIterations)
print("objectiveHistory: %s" % str(trainingSummary.objectiveHistory))
trainingSummary.residuals.show()
print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
print("r2: %f" % trainingSummary.r2)
```

---

```python

```
