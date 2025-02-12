from fastapi import FastAPI
from pyspark.ml.recommendation import ALSModel
from pyspark.sql import SparkSession
import psycopg2

app = FastAPI()

# Initialize Spark session & load ALS model
spark = SparkSession.builder.appName("RecommendationAPI").getOrCreate()
model = ALSModel.load("model_serving/als_model")

# PostgreSQL Connection
DATABASE_URL = "dbname=recommendations user=postgres password=yourpassword host=localhost port=5432"

def get_user_data(user_id):
    """Retrieve aggregated user features from PostgreSQL."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Fetch user features (clicks, views, purchases, searches)
    cursor.execute("SELECT * FROM user_features WHERE user_id = %s", (user_id,))
    user_features = cursor.fetchone()

    conn.close()
    return user_features

@app.get("/recommend/{user_id}")
def recommend_based_on_features(user_id: str):
    """Provide recommendations using ALS model with aggregated features."""
    user_features = get_user_data(user_id)

    if not user_features:
        return {"message": "No user features found", "recommendations": []}

    # Convert user_id into a DataFrame for Spark ALS model
    user_df = spark.createDataFrame([(user_id,)], ["user_id"])

    # Generate ALS recommendations
    recommendations = model.recommendForUserSubset(user_df, 5)

    return {
        "user_features": {
            "clicks": user_features[1],
            "views": user_features[2],
            "purchases": user_features[3],
            "search_count": user_features[4]
        },
        "recommended_products": recommendations.toJSON().collect()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
