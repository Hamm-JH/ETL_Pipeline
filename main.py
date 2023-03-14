
def req_data(url):
    """ url을 받아서 json 형태로 반환하는 함수 """
    import requests

    response = requests.get(url)

    return response.json()

def decrypt_data(key, data):
    """ 대칭키와 암호화된 데이터를 받아서 복호화된 데이터를 반환하는 함수 """
    from cryptography.fernet import Fernet

    _fernet = Fernet(key)

    return _fernet.decrypt(data)

def timestamp_to_datetime(timestamp):
    """ 타임스탬프를 datetime으로 변환하는 함수 """
    import datetime

    return datetime.datetime.fromtimestamp(timestamp)

# ----------------------------------------------------------------------------------------------

# requests 모듈을 사용하여 데이터를 가져온다.
url = "http://ec2-3-37-12-122.ap-northeast-2.compute.amazonaws.com/api/data/log"
data = req_data(url)

# print(data[0])
# print(data[0]['recordId'])
# print(data[0]['ArrivalTimeStamp'])
print(data[0]['data']) # 복호화 대상

# for i in data:
#     print(i['recordId'])
#     # print(i['ArrivalTimeStamp'])
#     # print(i['data'])

# ----------------------------------------------------------------------------------------------

# 미리 주어진 대칭키를 이용한 복호화를 수행한다. (샘플)
key = b't-jdqnDewRx9kWithdsTMS21eLrri70TpkMq2A59jX8='
decrypt_str = decrypt_data(key, data[0]['data'])
print(decrypt_str)

# ----------------------------------------------------------------------------------------------

timestamp = data[0]['ArrivalTimeStamp']

# 타임스탬프를 datetime으로 변환 (decrypt_str['inDate']의 값과 동일함)
datetime = timestamp_to_datetime(timestamp)
print(datetime)


# print(decrypt_str.decode('utf-8'))
