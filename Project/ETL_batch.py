from ETL_JO import ETL_JO
from pyspark.sql.types import *
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('Spark App').getOrCreate()

AWS_SERVICE_NAME = 's3'
REGION = "ap-northeast-2"

AWS_ACCESS_ID = 'aws_access_key_id'
AWS_SECRET_KEY = 'aws_secret_access_key'
AWS_BUCKET_NAME = 'aws_s3_bucket_name'

etl = ETL_JO()

data = etl._get_data()

# spark eda code


