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

# print(private_data)
print(private_data['aws_access_key_id'])
print(private_data['aws_secret_access_key'])