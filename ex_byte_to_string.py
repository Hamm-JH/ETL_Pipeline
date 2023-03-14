
bStr = b"{'user_id': 'ebda43f475bb8d35cc18c3dd7b8115cab2bed892c2588b70c42feae58c02dd40', 'record_id': 5822, 'activity': 'view', 'url': '/api/products/product/', 'method': 'POST', 'name': 'json_logger', 'inDate': '2023-03-10T01:48:11.818Z', 'detail': {'message': 'POST view', 'levelname': 'INFO'}}" 
print(bStr)

Str = bStr.decode('utf-8')
print(Str)