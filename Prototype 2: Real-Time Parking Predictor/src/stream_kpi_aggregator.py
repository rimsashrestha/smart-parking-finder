from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, count, expr
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

# Start Spark Session
spark = SparkSession.builder \
    .appName("ParkingKPIAggregator") \
    .getOrCreate()

# Define schema for the incoming JSON
schema = StructType([
    StructField("post_id", StringType()),
    StructField("street_name", StringType()),
    StructField("street_num", IntegerType()),
    StructField("latitude", DoubleType()),
    StructField("longitude", DoubleType()),
    StructField("analysis_neighborhood", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("occupied", IntegerType()),  # 1 for occupied, 0 for available
    StructField("hour", IntegerType()),
    StructField("dayofweek", IntegerType()),
    StructField("is_weekend", IntegerType())
])

# Read stream from Kafka
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "parking_predictions") \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON payload
json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Compute Occupancy Rate KPI (per 5 minutes window per neighborhood)
kpi_df = json_df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("analysis_neighborhood")
    ).agg(
        (avg(col("occupied")) * 100).alias("occupancy_rate_percentage"),
        count("*").alias("total_records")
    )

# Output the KPI to the console (or you can write to Kafka, PostgreSQL, etc.)
query = kpi_df.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
