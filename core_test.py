
# from Project.Core import Core

env_test = {
    "env" : "test",
    "url" : "localhost:8080",
    "aws" : {
        "aws_access_key_id":"aws_key",
        "aws_secret_access_key":"aws_secret",
        "aws_s3_bucket_name":"my_bucket"
    }
}

# core = Core("aaa")
# core.extract_url("aaa")

from Project.ETL_CP1 import ETL_CP1

etl = ETL_CP1(env_test)
etl.run(interval_minutes=1)

