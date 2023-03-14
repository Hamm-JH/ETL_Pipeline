
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

def str_to_json(str):
    """ 문자열을 json으로 변환하는 함수 """
    import json

    return json.loads(str.replace("'", "\""))

def encode_b64uuid_64(b64uuid):
    """ b64uuid를 uuid로 변환하는 함수 """
    from b64uuid import B64UUID

    start32 = B64UUID(b64uuid[:32])
    end32 = B64UUID(b64uuid[32:])

    return start32.string + end32.string

def convert_method_to_int(method):
    """ method를 int로 변환하는 함수 """
    if method == 'POST':
        return 1
    elif method == 'GET':
        return 2
    elif method == 'PUT':
        return 3
    elif method == 'DELETE':
        return 4
    else:
        return 0

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
print()

# for i in data:
#     print(i['recordId'])
#     # print(i['ArrivalTimeStamp'])
#     # print(i['data'])

# ----------------------------------------------------------------------------------------------
# 미리 주어진 대칭키를 이용한 복호화를 수행한다. (샘플)

key = b't-jdqnDewRx9kWithdsTMS21eLrri70TpkMq2A59jX8='
decrypt_str = decrypt_data(key, data[0]['data']).decode('utf-8')
print(decrypt_str); print()

# ----------------------------------------------------------------------------------------------
# 복호화된 데이터를 json(dict)으로 변환한다.

_json = str_to_json(decrypt_str)
print(_json)
print(type(_json))
print(_json['user_id']) # user_id : b64uuid 사용해서 축소할 예정
print(_json['record_id'])
print(_json['activity'])
print(_json['url'])
print(_json['method']) # method : POST, GET, PUT, DELETE, 1,2,3,4로 변환할 예정
print(_json['name'])
print(_json['inDate']) # inDate : datetime -> timestamp로 변환할 예정
print(_json['detail'])

# ----------------------------------------------------------------------------------------------
# uuid64 -> 문자열 길이 44만큼 축소

_json['user_id'] = encode_b64uuid_64(_json['user_id'])
# print(_json['user_id'])

# ----------------------------------------------------------------------------------------------
# method : POST, GET, PUT, DELETE, 1,2,3,4로 변환

_json['method'] = convert_method_to_int(_json['method'])
# print(_json['method'])

# ----------------------------------------------------------------------------------------------

# timestamp = data[0]['ArrivalTimeStamp']

# # 타임스탬프를 datetime으로 변환 (decrypt_str['inDate']의 값과 동일함)
# datetime = timestamp_to_datetime(timestamp)
# print(datetime)

# # # 연, 월, 일, 시, 분을 출력, 데이터 저장시 사용
# # print(datetime.year)
# # print(datetime.month)
# # print(datetime.day)
# # print(datetime.hour)
# # print(datetime.minute)

# # ----------------------------------------------------------------------------------------------

# from b64uuid import B64UUID

# # print(decrypt_str.decode('utf-8'))
