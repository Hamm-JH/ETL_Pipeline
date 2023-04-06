
# -----------------------------------------------------------------------------
# converts_

def convert_single_data(data):
    """ 하나의 데이터를 받아서 변환을 수행하고 결과를 반환한다. """
    import modules.cryptography_ as crypto
    import modules.json_ as json_
    import modules.b64uuid_ as b64
    import modules.converts_ as conv
    import modules.times_ as times

    # 1 미리 주어진 대칭키를 이용한 복호화를 수행한다.
    key = b't-jdqnDewRx9kWithdsTMS21eLrri70TpkMq2A59jX8='
    decrypt_str = crypto.decrypt(key, data['data']).decode('utf-8')
    # print(decrypt_str); print()

    # 2 복호화된 데이터를 json(dict)으로 변환한다.
    _json = json_.str_to_json(decrypt_str)
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
    _json['user_id'] = b64.encode_b64uuid_64(_json['user_id'])
    # print(_json['user_id'])

    # 4 method : POST, GET, PUT, DELETE, 1,2,3,4로 변환
    _json['method'] = conv.convert_method_to_int(_json['method'])
    # print(_json['method'])

    # 5 inDate : string(datetime) -> timestamp로 변환
    _json['inDate'] = times.string_to_timestamp(_json['inDate'])
    # print(_json['inDate'])

    return _json

# -----------------------------------------------------------------------------
# json_

# TODO : json 파일 위치가 변경이 필요하기 때문에 수정 대기
def get_private_data():
    """ 개인 데이터를 가져오는 함수 """
    import json

    with open('env/private.json', 'r') as f:
        data = json.load(f)
    
    return data

# -----------------------------------------------------------------------------
# feat : scheduling

def schedule_job():
    """ 스케쥴링을 수행하는 함수 """
    import modules.requests_ as req

    import modules.compress_ as compress
    import modules.aws_ as aws

    import datetime
    
    print(f'start schedule job : {datetime.datetime.now()}')

    # requests 모듈을 사용하여 데이터를 가져온다.
    url = "http://ec2-3-37-12-122.ap-northeast-2.compute.amazonaws.com/api/data/log"
    data = req.request(url)

    _data = {}

    # 먼저 데이터를 분할한다.
    # 파일 패스를 키값으로 설정
    for i in data:
        import modules.times_ as times

        # print(i['recordId']) # ex) 5822
        # print(i['ArrivalTimeStamp']) # ex) 1678412891.818
        # print(i['data']) # ex) [암호화된 데이터]

        # 미리 주어진 대칭키를 이용한 복호화를 수행한다.
        # 복호화된 데이터를 json(dict)으로 변환한다.
        # 각 데이터에서 개별적으로 변환이 필요한 부분에 변환을 수행한다.
        _json = convert_single_data(i)

        # # 데이터를 압축한다.
        # _compress = compress_dict(_json)
        # # print(_compress) # bytes
        # # print(len(_compress)) # zlib : 196 / gzip : 208

        # 타임스탬프를 datetime으로 변환 (decrypt_str['inDate']의 값과 동일함)
        datetime = times.timestamp_to_datetime(i['ArrivalTimeStamp'])

        # 연, 월, 일, 시를 출력, 데이터 저장시 사용
        times = [datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute, datetime.second, datetime.microsecond // 1000]
        # print(times); print()

        # 키로 사용
        path = f"data/{times[0]}/{times[1]}/{times[2]}/{times[3]}/"
        # print(path); print()

        if path in _data:
            _data[path].append(_json)
        else:
            _data[path] = [_json]

    # print(_data)
    for i in _data:
        # print(i)  # i : 파일 패스
        # print(_data[i]) # _data[i] : 파일 패스에 해당하는 데이터 리스트

        # 데이터를 압축한다.
        _compress = compress.compress_dict(_data[i])
        # print(_compress) # bytes
        # print(len(_compress)) # zlib : 196 / gzip : 208

        filepath = i+'log.txt'

        accessParams = get_private_data()

        aws.send_to_aws_s3_path(_compress, filepath, accessParams)

    print('finish schedule job')

# -----------------------------------------------------------------------------
# main

from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == "__main__":
    # scheduler = BlockingScheduler()
    
    # scheduler.add_job(schedule_job, 'interval', seconds=600)

    # scheduler.start()

    schedule_job()
