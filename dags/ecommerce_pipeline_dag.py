from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append('/opt/airflow/scripts')

from load_raw_data import load_raw_tables
from transform import run_transformation
from validate import validate_raw_orders, validate_star_schema

default_args = {
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='ecommerce_sales_pipeline',
    default_args=default_args,
    schedule='@daily',
    start_date=datetime(2026, 7, 1),
    catchup=False,
    tags=['ecommerce', 'portfolio'],
) as dag:

    extract_load_raw = PythonOperator(
        task_id='extract_load_raw',
        python_callable=load_raw_tables,
    )

    validate_raw = PythonOperator(
        task_id='validate_raw',
        python_callable=validate_raw_orders,
    )

    transform_star_schema = PythonOperator(
        task_id='transform_star_schema',
        python_callable=run_transformation,
    )

    validate_fact = PythonOperator(
        task_id='validate_fact',
        python_callable=validate_star_schema,
    )

    extract_load_raw >> validate_raw >> transform_star_schema >> validate_fact