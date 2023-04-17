import sys
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

module_directiory = "슬기님환경의project폴더경로\Project"
if module_directiory not in sys.path:
    sys.path.append(module_directiory)

from ETL_SG import ETL_SG


with DAG(
    "etl_pipeline4",
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=3),
        'wait_for_downstream': True,
    },

    description="ETL Pipeline",
    schedule=timedelta(days=1),
    start_date=datetime(2023, 4, 16),
    catchup=False,
    tags=["ETL"],
) as dag:
    
    def etl():
        AWS_SERVICE_NAME = 's3'
        REGION = "ap-northeast-2"

        AWS_ACCESS_ID = 'aws_access_key_id'
        AWS_SECRET_KEY = 'aws_secret_access_key'
        AWS_BUCKET_NAME = 'aws_s3_bucket_name'

        etl = ETL_SG()

        flattened_data = etl._extract_data(date)

        def partitioning(flattened_data):
            if len(flattened_data) != 0:
                year = flattened_data[0]['ADJ_DT'][0:4]
                month = flattened_data[0]['ADJ_DT'][4:6]
                date = flattened_data[0]['ADJ_DT']

                directory = f'{year}/{month}/{date}.json.gz'

                return flattened_data, directory

        etl._load_data(flattened_data, AWS_SERVICE_NAME, REGION, AWS_ACCESS_ID, AWS_SECRET_KEY, AWS_BUCKET_NAME, partitioning)


    t1 = PythonOperator(
        task_id="extract",
        python_callable=etl,
        dag=dag,
    )

    t1