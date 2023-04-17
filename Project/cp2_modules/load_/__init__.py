def s3_load(data, aws_service_name, region, aws_access_id, aws_secret_key, aws_bucket_name, partitioning_func = None):
    '''
    파티셔닝 후 저장하는 함수
    aws 파라미터 입력값은 str
    '''
    import json
    import os
    import gzip
    from modules import compress_
    from dotenv import load_dotenv
    load_dotenv()

    def s3_connection(aws_service_name, region, aws_access_id, aws_secret_key):
        '''
        aws S3에 연결하는 함수
        파라미터 입력값은 str
        '''
        import os
        import boto3
        from dotenv import load_dotenv
        load_dotenv()

        aws_access_key_id = os.getenv(aws_access_id)
        aws_secret_access_key = os.getenv(aws_secret_key)

        try:
            s3 = boto3.client(
                service_name= aws_service_name,
                region_name= region,
                aws_access_key_id = aws_access_key_id,
                aws_secret_access_key = aws_secret_access_key,
            )
        except Exception as e:
            print(e)
        else:
            print("s3 bucket connected!") 
            return s3

    if partitioning_func:
        data, directory = partitioning_func(data)
        compressed_data = compress_.compress(data)
            
        s3 = s3_connection(aws_service_name, region, aws_access_id, aws_secret_key)
        aws_s3_bucket_name = os.getenv(aws_bucket_name)
        s3.put_object(
            Bucket = aws_s3_bucket_name,
            Body = compressed_data,
            Key = directory,
            )
        
    else:
        s3 = s3_connection(aws_service_name, region, aws_access_id, aws_secret_key)
        aws_s3_bucket_name = os.getenv(aws_bucket_name)
        compressed_data = compress_.compress(data)

        s3.put_object(
            Bucket = aws_s3_bucket_name,
            Body = compressed_data,
            Key = directory,    # 디렉토리 설정 코드 필요
            )