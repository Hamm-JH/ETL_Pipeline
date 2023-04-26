from ETL_JO import ETL_JO
from pyspark.sql.types import *
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('Spark_EDA').getOrCreate()

AWS_SERVICE_NAME = 's3'
REGION = "ap-northeast-2"

AWS_ACCESS_ID = 'aws_access_key_id'
AWS_SECRET_KEY = 'aws_secret_access_key'
AWS_BUCKET_NAME = 'aws_s3_bucket_name'

etl = ETL_JO()

data = etl._get_data('20230407', AWS_ACCESS_ID, AWS_SECRET_KEY, AWS_BUCKET_NAME, REGION)

df = spark.createDataFrame(data)

def spark_EDA(spark_dataframe):
    re_list1 = ['감귤(기타)', '감귤(하우스)', '감귤 기타', '만다린(수)', '감자(기타)', '감자(수입)', '감자(단오)', '감자(조풍)', '감자수입', '딸기(기타)', '딸기', '딸기기타', '흰딸기', '버섯', '버섯기타', '사과', '후브락스(사과)', '사과(기타)', '가지고추', '퍼펙트고추', '블랙망고수박']
    re_list2 = ['카라향', '천혜향']
    re_list3 = ['금감']

    spark_dataframe = spark_dataframe.replace(re_list1, '기타', 'PUMJONG')
    spark_dataframe = spark_dataframe.replace(re_list2, '향', 'PUMJONG')
    spark_dataframe = spark_dataframe.replace(re_list3, 'replace 테스트', 'PUMJONG')

    return spark_dataframe


df_spark_EDA = spark_EDA(df)

df_spark_EDA.show()
# spark eda code


