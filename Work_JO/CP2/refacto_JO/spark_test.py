import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import *
from modules import extract_, compress_, load_
import pandas as pd

test = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
test_df = pd.DataFrame(test)

print(test_df)

spark_DF = SparkSession.builder.appName('DF_test').getOrCreate()
df = spark_DF.createDataFrame(test_df)
df.show()

spark_DF.stop()