from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

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
            import os
            import gzip
            import json
            import boto3
            from datetime import timedelta, datetime
            from time import sleep
            from dotenv import load_dotenv
            load_dotenv()

            from ETL_SG import ETL_SG


            AWS_SERVICE_NAME = 's3'
            REGION = "ap-northeast-2"

            AWS_ACCESS_ID = 'aws_access_key_id'
            AWS_SECRET_KEY = 'aws_secret_access_key'
            AWS_BUCKET_NAME = 'aws_s3_bucket_name'

            etl = ETL_SG()

            today = datetime.today()

            yesterday = (today - timedelta(days=1)).strftime('%Y%m%d')

            date = '20230415'

            flattened_data = etl._extract_data(yesterday)

            if len(flattened_data) != 0:
                year = flattened_data[0]['ADJ_DT'][0:4]
                month = flattened_data[0]['ADJ_DT'][4:6]
                date = flattened_data[0]['ADJ_DT']

                directory = f'{year}/{month}/{date}.json.gz'

            aws_access_key_id = os.getenv(AWS_ACCESS_ID)
            aws_secret_access_key = os.getenv(AWS_SECRET_KEY)

            try:
                s3 = boto3.client(
                    service_name= AWS_SERVICE_NAME,
                    region_name= REGION,
                    aws_access_key_id = aws_access_key_id,
                    aws_secret_access_key = aws_secret_access_key,
                )
            except Exception as e:
                print(e)
            else:
                print("s3 bucket connected!") 

            compressed_data = gzip.compress(json.dumps(flattened_data, ensure_ascii=False, indent=4).encode('utf-8'))
            
            aws_s3_bucket_name = os.getenv(AWS_BUCKET_NAME)
            
            s3.put_object(
                Bucket = aws_s3_bucket_name,
                Body = compressed_data,
                Key = directory,
                )


    t1 = PythonOperator(
        task_id="extract",
        python_callable=etl,
        dag=dag,
    )

    t1