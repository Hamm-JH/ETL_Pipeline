import sys
import os
sys.path.append(os.path.pardir)

import json

# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Construct the path to the private.json file
private_json_path = os.path.join(parent_dir, 'env/private.json')

# Open the file and load the JSON data
with open(private_json_path, 'r') as f:
    private_data = json.load(f)



import boto3

aws_access_key_id=private_data['aws_access_key_id']
aws_secret_access_key=private_data['aws_secret_access_key']

s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Specify the S3 bucket and file name
bucket_name = private_data['aws_s3_bucket_name']
file_name = 'data/your_file_name4'

# The string data to upload
string_data = 'your_string_data'

# Upload the string data to S3
s3.Object(bucket_name, file_name).put(Body=string_data)