import zlib
import json

# create a sample dictionary
data = {"key1": "value1", "key2": "value2", "key3": "value3"}

# -----

# serialize the dictionary to a JSON string
json_data = json.dumps(data)

# compress the serialized data
compressed_data = zlib.compress(json_data.encode())

# print the compressed data
print(compressed_data)

# -----

# decompress the data
decompressed_data = zlib.decompress(compressed_data)

# deserialize the JSON string to a dictionary
result = json.loads(decompressed_data.decode())

# print the result
print(result)