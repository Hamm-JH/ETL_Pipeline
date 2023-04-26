from ETL_SG import ETL_SG
# from pyspark.sql.types import *
# from pyspark.sql import SparkSession


AWS_SERVICE_NAME = 's3'
REGION = "ap-northeast-2"

AWS_ACCESS_ID = 'aws_access_key_id'
AWS_SECRET_KEY = 'aws_secret_access_key'
AWS_BUCKET_NAME = 'aws_s3_bucket_name'

etl = ETL_SG()

def partitioning(flattened_data):
    if len(flattened_data) != 0:
        year = flattened_data[0]['ADJ_DT'][0:4]
        month = flattened_data[0]['ADJ_DT'][4:6]
        date = flattened_data[0]['ADJ_DT']

        directory = f'{year}/{month}/{date}.json.gz'

        return flattened_data, directory


def etl_stream(date):
    flattened_data = etl._extract_data(date)

    # schema 설정
    # sparkSession open

    # spark 처리 코드 작성가능

    etl._load_data(flattened_data, AWS_SERVICE_NAME, REGION, AWS_ACCESS_ID, AWS_SECRET_KEY, AWS_BUCKET_NAME, partitioning)
        
etl_stream('20230407')

# spark.stop()
    