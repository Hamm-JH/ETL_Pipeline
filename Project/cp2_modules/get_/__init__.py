def get_json(date, aws_access_key_id, aws_secret_access_key, aws_s3_bucket_name, region):
    '''
    aws S3 에서 파일을 불러온 뒤
    gzip 압축을 풀고 json 데이터를 반환하는 함수
    입력값은 str
    '''
    import boto3
    import os
    import gzip
    import json
    from dotenv import load_dotenv
    load_dotenv()

    aws_access_key_id = os.getenv(aws_access_key_id)
    aws_secret_access_key = os.getenv(aws_secret_access_key)
    aws_s3_bucket_name = os.getenv(aws_s3_bucket_name)

    s3 = boto3.client(
                service_name="s3",
                region_name=region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )

    year = date[0:4]
    month = date[4:6]

    obj = s3.get_object(
        Bucket = aws_s3_bucket_name,
        Key = f'{year}/{month}/{date}.json.gz'
    )

    with gzip.GzipFile(fileobj=obj.get('Body'), mode='r') as gz:
        content = gz.read()

    json_data = json.loads(content)

    
    import pandas as pd
    df = pd.DataFrame(json_data)
    
    return df