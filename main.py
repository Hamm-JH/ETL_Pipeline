
def req_data(url):
    """ url을 받아서 json 형태로 반환하는 함수 """
    import requests

    response = requests.get(url)

    return response.json()

url = "http://ec2-3-37-12-122.ap-northeast-2.compute.amazonaws.com/api/data/log"
data = req_data(url)


# print(data[0])
# print(data[0]['recordId'])
# print(data[0]['ArrivalTimeStamp'])
print(data[0]['data']) # 복호화 대상
print()
print()
print()

# for i in data:
#     print(i['recordId'])
#     # print(i['ArrivalTimeStamp'])
#     # print(i['data'])

# from cryptography.fernet import Fernet
# key = Fernet.generate_key()
# print(f"대칭키:{key}")

# fernet = Fernet(key)

# decrypt_str = fernet.decrypt(data[0]['data'].encode())

# print(decrypt_str)

from cryptography.fernet import Fernet
# key = Fernet.generate_key()
key = b't-jdqnDewRx9kWithdsTMS21eLrri70TpkMq2A59jX8='
print(f"대칭키:{key}")

fernet = Fernet(key)
# json_log = {"url": "/api/products/product/24", "method": "DELETE", "product_id": 24, "user_id": 21, "name": "log_file2", "inDate": "2022-12-01T01:32:21.437Z", "detail": {"message": "DELETE access Board Detail", "levelname": "INFO"}}
# encrypt_str = fernet.encrypt(f"{json_log}".encode('ascii'))
# print("암호화된 문자열:", encrypt_str)

# decrypt_str = fernet.decrypt(encrypt_str)
# print("복호화된 문자열: ", decrypt_str)

decrypt_str = fernet.decrypt(data[0]['data'])
print(decrypt_str)
