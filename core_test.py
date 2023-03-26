
from Project.Core import Core

env_test = {
    "env" : "test",
    "url" : "localhost:8080"
}

# core = Core("aaa")
# core.extract_url("aaa")

from Project.ETL_CP1 import ETL_CP1

etl = ETL_CP1(env_test)
etl.extract_url("aaa")
