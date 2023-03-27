import os
import json
import requests
import boto3
import uuid
import base64
import gzip
import value_comp
import importlib       # method_trans 비교를 위한 모듈(모듈 재호출 기능)
from datetime import datetime
from cryptography.fernet import Fernet
from b64uuid import B64UUID
from dotenv import load_dotenv  # Private_key(환경변수) 보안 모듈
load_dotenv()
from apscheduler.schedulers.blocking import BlockingScheduler

url = 'http://ec2-3-37-12-122.ap-northeast-2.compute.amazonaws.com/api/data/log'
key = b't-jdqnDewRx9kWithdsTMS21eLrri70TpkMq2A59jX8='

JSON_LOG_PATH = './json_log.json'
VALUE_DICT_PATH = './value_comp.py'
COMP_LOG_PATH = './comp_log.json'
S3_BUCKET = os.getenv('S3_BUCKET')

# api 요청으로 json_log 받기
def get_json_log(url):
    json_log = requests.get(url).json()
    return json_log

# 이미 이전에 받은 데이터는 제외하고 새로운 데이터만 반환
def except_duplicate(input, log_exist):
    for i in log_exist:
        if i['recordId'] == input:
            return False
    return True

# 받은 json_log 저장
def save_json_log(filepath, log):
    # 받은 json_log 중 이미 받았던 로그(중복제외) 제외 새로운 log만 할당함
    new_log = []
    # path 를 가진 파일(로그가 저장된 파일)이 없을 경우, log 저장할 파일 생성
    if not os.path.isfile(filepath):
        with open(filepath, 'w') as f:
            json.dump(log, f, indent = 2)
        # 이 경우, 받은 json_log 전체가 새로운 log
        new_log = log
    # path 를 가진 파일 있을 경우, 해당 파일에 이어서 log 저장
    else:
        with open(filepath, 'r') as f:
            log_exist = json.load(f)
        for i in log:
            if except_duplicate(i['recordId'], log_exist):
                log_exist.append(i)
                # 이 경우, 받은 json_log 중 중복 제외하고 새로운 log 에 할당
                new_log.append(i)
        with open(filepath, 'w') as f:
            json.dump(log_exist, f, indent = 2)
    return new_log

# 받은 log의 암호화된 데이터 복호화, 문자열 압축 알고리즘 적용 후 다시 암호화 및 저장
# 1. 암호화된 부분 복호화
# 2. b64uuid 모듈을 사용하여 'user_id' 64(32 / 32) 자 -> 44(22 /22) 자 압축
# 3. 'method' 를 value 별 숫자로 압축
# 4. 'url' 을 value 별 숫자로 압축
# 5. 'inDate' 다른 표기방식으로 압축
# 6. 암호화
# 7. 파일 저장(.json)
# 8. gzip 압축 파일 생성
# + '년도/월/일/시(1시간 단위)' 로 data partitioning
# 8-1. 받은 comp_log 를 data partitioning
# 8-2. partitioning 된 log 를 압축 


# 1. 암호화된 부분 복호화
def decrypt_data(log, key):
    fernet = Fernet(key)
    for i in log:
        decrypted_data = fernet.decrypt(i['data']).decode('ascii')
        i['data'] = decrypted_data
        # replace 로 ' -> " 를 변환해주는 이유는 json 모듈이 key 나 value 를 문자열로 인식하기 때문
        # json 모듈의 인식가능한 문자열은 반드시 ""로 감싸여져 있어야 한다(JavaScript 에서 유래된 모듈이다)
        # 문자열로 이루어진 'data' 의 복호화된 문자열 내부 data를 dict 로 변환
        i['data'] = json.loads(i['data'].replace("'", "\""))
    return

# 2. b64uuid 모듈을 사용하여 'user_id' 64(32 / 32) 자 -> 44(22 /22) 자 압축
def to_b64uuid(log):
    for i in log:
        i['data']['user_id'] = B64UUID(i['data']['user_id'][:32]).string + B64UUID(i['data']['user_id'][32:]).string
    return

# 3. 'method' 를 value 별 숫자로 압축
# 'method' 의 value 별 숫자를 저장한 dict를 사용
# 새로운 method 가 등장할 때 마다, 변환 후 업데이트
def comp_method(log, dict):
    for i in log:
        item = i['data']['method']
        # 호출된 dict 에 값이 없는 경우(새로운 method)
        if item not in dict:
            # dict 가 비어있으면 새로운 값에 1 할당
            if dict == {}:
                dict[item] = 1
            # dict 에 다른 값이 있으면 새로운 값에 마지막 숫자 + 1 할당
            else:
                dict[item] = len(dict) + 1
            i['data']['method'] = dict[item]
        # 호출된 dict 에 값이 있는 경우
        else:
            i['data']['method'] = dict[item]
    return

# 4. 'url' 을 value 별 숫자로 압축
# '/api/products/product/' 를 base로, 다음에 붙는 숫자를 value 로 압축
# base 만 있으면(숫자가 없으면) base : 0 할당
# 'method' 압축과 마찬가지로 진행
def comp_url(log, dict):
    for i in log:
        item = i['data']['url']
        # 호출된 dict 에 값이 없는 경우(새로운 url)
        if item not in dict:
            # base 만 존재하면, 0 할당
            if len(item) == 22:
                dict[item] = 0
            # base + 숫자 구성 이면, 해당 숫자 할당
            else:
                dict[item] = int(item[22:])
            i['data']['url'] = dict[item]
        # 호출된 dict 에 값이 있는 경우
        else:
            i['data']['url'] = dict[item]
    return

# 5. 'inDate' 다른 표기방식으로 압축 / 'inDate' key 추가
def trans_indate_plus(data):
    for i in data:
        inDate = i['data']['inDate']
        date = datetime.fromisoformat(inDate[:-1])
        outDate = date.strftime('%y%m%d%H%M%S%f')
        i['data']['inDate'] = outDate
        i['inDate'] = outDate

# 6. 암호화
def encrypt_data(log):
    for i in log:
        json_log = i['data']
        fernet = Fernet(key)
        encrypt_str = fernet.encrypt(f'{json_log}'.encode('ascii'))
        i['data'] = encrypt_str.decode()

# 7. 압축 처리한 log, 새로운 파일에 저장(.json)
# 중복된 recordId 는 앞에서 처리 했기 때문에, 중복체크 필요없음
def save_comp_log(filepath, log):
    # 의미없는 key 삭제
    for i in log:
        i.pop('recordId', None)
        i.pop('ArrivalTimeStamp', None)
    # path 를 가진 파일(로그가 저장된 파일)이 없을 경우, log 저장할 파일 생성
    if not os.path.isfile(filepath):
        with open(filepath, 'w') as f:
            json.dump(log, f, indent = 2)
    # path 를 가진 파일 있을 경우, 해당 파일에 이어서 log 저장
    else:
        with open(filepath, 'r') as f:
            log_exist = json.load(f)
            log_exist.extend(log)
        with open(filepath, 'w') as f:
            json.dump(log_exist, f, indent = 2)
    return log

# 8. gzip 압축 파일 생성
def log_to_gzip(log):
    data = {}       # comp_log 를 파티셔닝하여 분류할 dict 생성

    # 8-1. 받은 comp_log 를 data partitioning
    # key 를 '년도/월/일/시(1시간 단위)', value 를 해당하는 log 리스트로 분류
    for item in log:
        inDate = item['inDate'][:8]
        if inDate in data:
            data[inDate].append(item)
        else:
            data[inDate] = [item]

    # 8-2. partitioning 된 log 를 압축
    for i in data:
        # 파티셔닝 된 시간대로 파일명 지정
        filepath = f"./gzip_log/{i}.gz"

        # 압축한 적 없는 새로운 시간대의 log일 경우 새로운 압축파일 생성
        if not os.path.isfile(filepath):
            with gzip.open(filepath, 'wb') as f:
                gzip_log = json.dumps(data[i]).encode('utf-8')
                f.write(gzip_log)

        # 해당 시간대의 압축파일이 이미 있는경우, 업데이트
        else:
            with gzip.open(filepath, 'rb') as f:
                gzip_exist = f.read()
                log_exist = json.loads(gzip_exist.decode('utf-8'))
                log_exist.extend(data[i])
            with gzip.open(filepath, 'wb') as f:
                gzip_log = json.dumps(log_exist).encode('utf-8')
                f.write(gzip_log)
    return data

# ----------------------AWS S3 적재------------------------

# AWS S3 에 gzip 업데이트 & 업로드
# 1. AWS S3 연결
# 2. 파티셔닝된 log data 의 key를 이용하여 gzip 업데이트 & 업로드

# AWS S3 연결
def S3_connection():
    try:
        s3 = boto3.client(
            service_name = 's3',
            region_name = 'ap-northeast-2',
            aws_access_key_id = os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        )
    except Exception as e:
        print(e)
        print('---!!!S3 bucket connection Failed!!!---')
    else:
        print('---S3 bucket connected---')
        return s3
    
# 새로운 comp_log를 적재 / 변경된 gzip을 업데이트
# + comp_log 를 년도/월/일/시(1시간 단위) 로 data partitioning
def S3_load(data):
    s3 = S3_connection()

    for key in data:
        y = key[:2]
        m = key[2:4]
        d = key[4:6]
        h = key[6:8]
        load_path = f'data_partitioning/{y}/{m}/{d}/{h}/comp_log.gz'
        filename = f'./gzip_log/{key}.gz'

        s3.upload_file(filename, S3_BUCKET, load_path)

    print('New_Compressed_log(.gz) was uploaded to S3 BUCKET')
    



# ----------------------ETL_PIPELINE------------------------


def ETL_Pipeline():
    # json_log 받아오기
    json_log = get_json_log(url)
    # pipeline을 통해 전달될 새로운 log
    new_log = save_json_log(JSON_LOG_PATH, json_log)
    # update 된 log 없을 경우 종료
    if new_log == []:
        print('No log updated')
        return
    # new_log 갯수 확인
    print(f"There are '{len(new_log)}ea' new_log updated")
    
    # 암호화된 부분 복호화
    decrypt_data(new_log, key)
    # 'user_id' 압축
    to_b64uuid(new_log)
    # 'method' 압축
    comp_method(new_log, value_comp.method_dict)
    # 'url' 압축
    comp_url(new_log, value_comp.url_dict)
    # 'inDate' 압축
    trans_indate_plus(new_log)

    # 압축 후 (업데이트된) method_dict
    new_method_dict = value_comp.method_dict

    # 업데이트전(수정되지 않은 dict)의 원본 method_dict 호출
    importlib.reload(value_comp)
    old_method_dict = value_comp.method_dict

    # 원본 method_dict 와 압축 후 method_dict를 비교
    # 업데이트된 값이 있으면 원본 method_dict를 업데이트
    if old_method_dict != new_method_dict:
        with open(VALUE_DICT_PATH, 'r') as f:
            lines = f.readlines()
        # line[0] 의 method_dict 만 수정
        lines[0] = f'method_dict = {new_method_dict}\n' 

        with open(VALUE_DICT_PATH, 'w') as f:
            f.writelines(lines)

    # 압축 후 (업데이트된) url_dict
    new_url_dict = value_comp.url_dict

    # 업데이트전(수정되지 않은 dict)의 원본 url_dict 호출
    importlib.reload(value_comp)
    old_url_dict = value_comp.url_dict

    # 원본 url_dict 와 압축 후 url_dict를 비교
    # 업데이트된 값이 있으면 원본 url_dict를 업데이트
    if old_url_dict != new_url_dict:
        with open(VALUE_DICT_PATH, 'r') as f:
            lines = f.readlines()
        # line[1] 의 url_dict 만 수정
        lines[1] = f'url_dict = {new_url_dict}\n' 

        with open(VALUE_DICT_PATH, 'w') as f:
            f.writelines(lines)

    # 암호화
    encrypt_data(new_log)
    # comp_log 저장
    comp_log = save_comp_log(COMP_LOG_PATH, new_log)
    data = log_to_gzip(comp_log)      # comp_log 를 파티셔닝하여 분류한 log data
    
    # 압축 프로세스 정상 작동 확인
    print('---Successfully processed [Compression / Partitioning / Encryption]---')

    # AWS S3 적재
    S3_load(data)


# 파이프라인 스케쥴링
# APScheduler
# 3분 간격 upload
def ETL_schedule():
    # 프로그램 실행과 동시에 적재
    ETL_Pipeline()

    # 스케쥴링(3분)
    scheduler = BlockingScheduler()
    scheduler.add_job(ETL_Pipeline, 'interval', minutes=3)
    
    # 3분 간격 적재
    scheduler.start()

ETL_schedule()