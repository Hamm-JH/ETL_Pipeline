from Core import Core

class ETL_CP1(Core):
    """
    ETL_CP1 프로젝트용으로 작성한 클래스
    """
    def __init__(self, env):
        super().__init__(env)
    
    def _extract_url(self, url):
        import modules.requests_ as req

        return req.req_data(url)

    def _transform_data(self, data):
        """ 하나의 데이터를 받아서 변환을 수행하고 결과를 반환한다. """
        import modules.cryptography_ as crypto
        import modules.json_ as json_
        import modules.b64uuid_ as b64
        import modules.converts_ as conv
        import modules.times_ as times

        # 1 미리 주어진 대칭키를 이용한 복호화를 수행한다.
        key = b't-jdqnDewRx9kWithdsTMS21eLrri70TpkMq2A59jX8='
        decrypt_str = crypto.decrypt_data(key, data['data']).decode('utf-8')
        # print(decrypt_str); print()

        # 2 복호화된 데이터를 json(dict)으로 변환한다.
        _json = json_.str_to_json(decrypt_str)

        # 3 uuid64 -> 문자열 길이 44만큼 축소
        _json['user_id'] = b64.encode_b64uuid_64(_json['user_id'])

        # 4 method : POST, GET, PUT, DELETE, 1,2,3,4로 변환
        _json['method'] = conv.convert_method_to_int(_json['method'])

        # 5 inDate : string(datetime) -> timestamp로 변환
        _json['inDate'] = times.string_to_timestamp(_json['inDate'])

        return _json

    def _load_data(self, data, filepath, params):
        import modules.aws_ as aws
        aws.send_to_aws_s3_path(data, filepath, params)

    def _schedule_job(self):


        import modules.compress_ as compress
        import datetime

        # requests 모듈을 사용하여 데이터를 가져온다.
        url = self.env["url"]
        data = self.extract_url(url)

        _data = {}

        print(f'start schedule job : {datetime.datetime.now()}')

        # 먼저 데이터를 분할한다.
        # 파일 패스를 키값으로 설정
        for i in data:
            import modules.times_ as times

            _json = self.transform_data(i)

            # # s3에 저장된 데이터의 위치를 기록
            # 타임스탬프를 datetime으로 변환 (decrypt_str['inDate']의 값과 동일함)
            datetime = times.timestamp_to_datetime(i['ArrivalTimeStamp'])

            # 연, 월, 일, 시를 출력, 데이터 저장시 사용
            times = [datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute, datetime.second, datetime.microsecond // 1000]

            # 키로 사용
            path = f"data/{times[0]}/{times[1]}/{times[2]}/{times[3]}/"

            if path in _data:
                _data[path].append(_json)
            else:
                _data[path] = [_json]

        for i in _data:

            # 데이터를 압축한다.
            _compress = compress.compress_dict(_data[i])

            filepath = i+'log.txt'

            accessParams = self.env["aws"]

            self.load_data(_compress, filepath, accessParams)

        print('finish schedule job')

    def run(self, interval_minutes=1):
        import schedule
        import time

        # n분마다 스케쥴링
        schedule.every(interval_minutes).minutes.do(self._schedule_job)

        while True:
            schedule.run_pending()
            time.sleep(1)



    