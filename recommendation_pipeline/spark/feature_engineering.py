from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, lower

spark = SparkSession.builder.appName("FeatureEngineering").getOrCreate()

# Load user activity (clicks, views, purchases) from PostgreSQL
df_activity = spark.read.jdbc("jdbc:postgresql://localhost:5432/recommendations", "user_activity")

# Load search events & product catalog
df_search = spark.read.jdbc("jdbc:postgresql://localhost:5432/recommendations", "search_events")
df_products = spark.read.jdbc("jdbc:postgresql://localhost:5432/recommendations", "product_catalog")

# Map search queries to product IDs using LIKE for fuzzy matching
f_search = df_search.crossJoin(df_products) \
                     .filter(lower(df_products["product_name"]).contains(lower(df_search["search_query"]))) \
                     .select(df_search["user_id"], df_products["product_id"])

# Aggregate search count per user and product
search_features = f_search.groupBy("user_id", "product_id").agg(count("product_id").alias("search_count"))

# Aggregate user interaction features (clicks, views, purchases)
activity_features = df_activity.groupBy("user_id", "product_id").pivot("event_type").count().fillna(0)

# Merge both search & interaction features
user_features = search_features.join(activity_features, ["user_id", "product_id"], "outer").fillna(0)

# Store aggregated features in PostgreSQL
user_features.write.jdbc("jdbc:postgresql://localhost:5432/recommendations", "user_features", mode="overwrite")

print("User feature extraction with LIKE-based search aggregation completed.")
