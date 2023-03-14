
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

def datetime_to_timestamp(datetime):
    """ datetime을 타임스탬프로 변환하는 함수 """
    import time

    return time.mktime(datetime.timetuple())

def string_to_datetime(string):
    """ 문자열을 datetime으로 변환하는 함수 """
    import datetime

    return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%fZ')

def string_to_timestamp(string):
    """ 문자열을 타임스탬프로 변환하는 함수 """

    return datetime_to_timestamp(string_to_datetime(string))
    

def dump_data(data):
    """ 데이터를 파일로 저장하는 함수 """
    import json

    return json.dumps(data)

def compress_data(str_data):
    """ 데이터를 압축하는 함수 """
    import zlib
    return zlib.compress(str_data.encode())

    # import gzip
    # return gzip.compress(str_data.encode())

def compress_dict(dict_data):
    """ dict 데이터를 압축하는 함수 """
    return compress_data(dump_data(dict_data))

def convert_single_data(data):
    """ 하나의 데이터를 받아서 변환을 수행하고 결과를 반환한다. """

    # 1 미리 주어진 대칭키를 이용한 복호화를 수행한다.
    key = b't-jdqnDewRx9kWithdsTMS21eLrri70TpkMq2A59jX8='
    decrypt_str = decrypt_data(key, data['data']).decode('utf-8')
    # print(decrypt_str); print()

    # 2 복호화된 데이터를 json(dict)으로 변환한다.
    _json = str_to_json(decrypt_str)
    # print(_json)
    # print(type(_json))
    # print(_json['user_id']) # user_id : b64uuid 사용해서 축소할 예정
    # print(_json['record_id'])
    # print(_json['activity'])
    # print(_json['url'])
    # print(_json['method']) # method : POST, GET, PUT, DELETE, 1,2,3,4로 변환할 예정
    # print(_json['name'])
    # print(_json['inDate']) # inDate : datetime -> timestamp로 변환할 예정
    # print(_json['detail'])

    # 3 uuid64 -> 문자열 길이 44만큼 축소
    _json['user_id'] = encode_b64uuid_64(_json['user_id'])
    # print(_json['user_id'])

    # 4 method : POST, GET, PUT, DELETE, 1,2,3,4로 변환
    _json['method'] = convert_method_to_int(_json['method'])
    # print(_json['method'])

    # 5 inDate : string(datetime) -> timestamp로 변환
    _json['inDate'] = string_to_timestamp(_json['inDate'])
    # print(_json['inDate'])

    return _json



if __name__ == "__main__":
    # requests 모듈을 사용하여 데이터를 가져온다.
    url = "http://ec2-3-37-12-122.ap-northeast-2.compute.amazonaws.com/api/data/log"
    data = req_data(url)

    for i in data:
        # print(i['recordId']) # ex) 5822
        # print(i['ArrivalTimeStamp']) # ex) 1678412891.818
        # print(i['data']) # ex) [암호화된 데이터]

        # 미리 주어진 대칭키를 이용한 복호화를 수행한다.
        # 복호화된 데이터를 json(dict)으로 변환한다.
        # 각 데이터에서 개별적으로 변환이 필요한 부분에 변환을 수행한다.
        _json = convert_single_data(i)
        # print(_json); print()

        _compress = compress_dict(_json)
        print(_compress) # bytes
        # print(len(_compress)) # zlib : 196 / gzip : 208
        # print()

        # 타임스탬프를 datetime으로 변환 (decrypt_str['inDate']의 값과 동일함)
        datetime = timestamp_to_datetime(i['ArrivalTimeStamp'])

        # 연, 월, 일, 시를 출력, 데이터 저장시 사용
        times = [datetime.year, datetime.month, datetime.day, datetime.hour]
        # print(times); print()

        break

