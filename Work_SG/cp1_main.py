import requests
import json
from cryptography.fernet import Fernet
from b64uuid import B64UUID
import re
import gzip
import boto3
import os
import schedule
import time
from dotenv import load_dotenv
load_dotenv()

api_url = 'http://ec2-3-37-12-122.ap-northeast-2.compute.amazonaws.com/api/data/log'
api_key = b't-jdqnDewRx9kWithdsTMS21eLrri70TpkMq2A59jX8='

# 파싱된 데이터 복호화
def decrypt(key, data):
    fernet = Fernet(key)
    for i in range(len(data)):
        temp = fernet.decrypt(data[i]['data']).decode('utf-8').replace("'", "\"")
        data[i]['data'] = json.loads(temp)
    return data

# 복호화된 데이터 문자열 압축
def zip_str(data):
    for i in range(len(data)):
        user_id = data[i]['data']['user_id']
        short_id = B64UUID(user_id[:32]).string + B64UUID(user_id[32:]).string
        data[i]['data']['user_id'] = short_id

        method = data[i]['data']['method']
        if method == 'GET':
            data[i]['data']['method'] = 1
        elif method == 'POST':
            data[i]['data']['method'] = 2
        elif method == 'PUT':
            data[i]['data']['method'] = 3
        else:
            data[i]['data']['method'] = 4

        url = data[i]['data']['url']
        if url == '/api/products/product/':
            data[i]['data']['url'] = 1
        else:
            data[i]['data']['url'] = 0

        indate = data[i]['data']['inDate']
        data[i]['data']['inDate'] = re.sub("[^0-9]","",indate[2:])

    return data

# 데이터 나누기
def data_split(data):
    first_hour = data[0]['data']['inDate'][6:8]
    date_split = [0]

    for i in range(len(data)):
        next_hour = data[i]['data']['inDate'][6:8]
        if first_hour != next_hour:
            first_hour = next_hour
            date_split.append(i)
    date_split.append(100)

    result = []
    for i in range(len(date_split)-1):
        result.append(data[date_split[i]:date_split[i+1]])
    return result

# aws s3 연결
aws_access_key_id = os.environ.get('aws_access_key_id')
aws_secret_access_key = os.environ.get('aws_secret_access_key')
aws_s3_bucket_name = os.environ.get('aws_s3_bucket_name')

def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!") 
        return s3

# 데이터 업로드
def aws_upload(data):
    year = data[0][0]['data']['inDate'][0:2]
    month = data[0][0]['data']['inDate'][2:4]
    day = data[0][0]['data']['inDate'][4:6]
    hour = data[0][0]['data']['inDate'][6:8]
    minutes = data[0][0]['data']['inDate'][8:]

    save_directory = f'{year}/{month}/{day}/{hour}/{minutes}.json.gz'
    compressed_data = gzip.compress(json.dumps(data).encode('utf-8'))
    return save_directory, compressed_data

def etl_pipeline():
    page = requests.get(api_url)
    parsed_data = json.loads(page.text)

    decrypt_data = decrypt(api_key, parsed_data)
    zip_data = zip_str(decrypt_data)
    splited_data = data_split(zip_data)
    save_directory, compressed_data = aws_upload(splited_data)

    s3 = s3_connection()
    s3.put_object(
        Bucket = aws_s3_bucket_name,
        Body = compressed_data,
        Key = save_directory,
    )

schedule.every(5).minutes.do(etl_pipeline)
while True:
    schedule.run_pending()
    time.sleep(1)