from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import subprocess

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
}

dag = DAG(
    "full_recommendation_pipeline",
    default_args=default_args,
    schedule_interval="@daily",  # Runs every day
)

def extract_events_data():
    """Extract and aggregate search & user activity data."""
    subprocess.run(["python", "recommendation_pipeline/spark/feature_engineering.py"], check=True)

def train_model():
    """Train recommendation model using ALS."""
    subprocess.run(["python", "recommendation_pipeline/spark/model_training.py"], check=True)

restart_api = BashOperator(
    task_id="restart_api",
    bash_command="docker restart recommendation_api",
    dag=dag,
)

extract_events_task = PythonOperator(
    task_id="extract_events_data",
    python_callable=extract_events_data,
    dag=dag,
)

train_model_task = PythonOperator(
    task_id="train_recommendation_model",
    python_callable=train_model,
    dag=dag,
)

extract_events_task >> train_model_task >> restart_api
