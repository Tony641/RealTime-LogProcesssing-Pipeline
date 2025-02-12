from pyspark.ml.recommendation import ALS
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ModelTraining").getOrCreate()

# Load precomputed user features (including aggregated search & interactions)
df = spark.read.jdbc("jdbc:postgresql://localhost:5432/recommendations", "user_features")

# Create engagement score (searches + interactions)
df = df.withColumn("engagement_score", col("click") * 3 + col("view") * 1 + col("purchase") * 5 + col("search_count") * 2)

# Train ALS model using weighted implicit feedback
als = ALS(userCol="user_id", itemCol="product_id", ratingCol="engagement_score", implicitPrefs=True)
model = als.fit(df)

# Save trained model
model.save("model_serving/als_model")
print("ALS model training completed.")
