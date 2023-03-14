
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

from cryptography.fernet import Fernet
# key = Fernet.generate_key()
key = b't-jdqnDewRx9kWithdsTMS21eLrri70TpkMq2A59jX8='
print(f"대칭키:{key}")

fernet = Fernet(key)

decrypt_str = fernet.decrypt(data[0]['data'])
print(decrypt_str)
