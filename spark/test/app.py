from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, FloatType, StringType
import folium

spark = SparkSession.builder \
    .appName("Spark Geo Map") \
    .getOrCreate()

schema = StructType([
    StructField("latitude", FloatType(), nullable=False),
    StructField("longitude", FloatType(), nullable=False),
    StructField("info", StringType(), nullable=True)
])

data = [
    (41.8781, -87.6298, "Chicago, USA - Informazioni XYZ"),  
    (51.5074, -0.1278, "London, UK - Informazioni ABC"),   
    (35.6895, 139.6917, "Tokyo, Japan - Altre informazioni"),  
    (-33.8688, 151.2093, "Sydney, Australia - Altre informazioni"), 
    (40.7128, -74.0060, "New York City, USA - Altre informazioni")
]

df = spark.createDataFrame(data, schema)

latitudes = df.select("latitude").rdd.flatMap(lambda x: x).collect()
longitudes = df.select("longitude").rdd.flatMap(lambda x: x).collect()
infos = df.select("info").rdd.flatMap(lambda x: x).collect()

mymap = folium.Map(location=[latitudes[0], longitudes[0]], zoom_start=2)

for lat, lon, info in zip(latitudes, longitudes, infos):
    folium.Marker([lat, lon], popup=folium.Popup(info, parse_html=True)).add_to(mymap)

mymap.save("mymap.html")
