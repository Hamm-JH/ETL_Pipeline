import time
import os
from dotenv import load_dotenv
load_dotenv()
from modules import extract_, compress_, load_

start = time.time()
AWS_SERVICE_NAME = "s3"
REGION = "ap-northeast-2"
AWS_ACCESS_ID = 'aws_access_key_id'
AWS_SECRET_KEY = 'aws_secret_access_key'
AWS_BUCKET_NAME = 'aws_s3_bucket_name'

def transform(date):
    '''
    날짜를 입력하면 그 날짜의 모든 거래를 품목별 법인별로 집계하여\n
    단일 json 데이터로 반환하는 함수
    '''
    import math
    from dotenv import load_dotenv
    load_dotenv()

    api_id = os.environ.get('garak_id')
    api_pw = os.environ.get('garak_passwd')
    url = 'http://www.garak.co.kr/publicdata/dataOpen.do?'

    bubin_list = ['11000101','11000102','11000103','11000104','11000105','11000106']
    pummok_list = ['감귤','감자','건고추','고구마','단감','당근','딸기','마늘','무',
                    '미나리','바나나','배','배추','버섯','사과','상추','생고추','수박',
                    '시금치','양배추','양상추','양파','오이','참외','토마토','파',
                    '포도','피망','호박']

    dict1 = {'data': []}
    for pummok in pummok_list:
        dict2 = {f'{pummok}': []}
        for bubin in bubin_list:
            params = (
                    ('id', api_id),
                    ('passwd', api_pw),
                    ('dataid', 'data12'),
                    ('pagesize', '10'),
                    ('pageidx', '1'),
                    ('portal.templet', 'false'),
                    ('s_date', date),
                    ('s_bubin', bubin),
                    ('s_pummok', pummok),
                    ('s_sangi', '')
                    )
            dict3 = {f'{bubin}': []}
            list_total_count = int(extract_.extract(url, params)['lists']['list_total_count'])
            total_page = math.ceil(int(list_total_count) / 10)

            if int(list_total_count) != 0:
                for page in range(1, total_page+1):
                    params = (
                                ('id', api_id),
                                ('passwd', api_pw),
                                ('dataid', 'data12'),
                                ('pagesize', '10'),
                                ('pageidx', page),
                                ('portal.templet', 'false'),
                                ('s_date', date),
                                ('s_bubin', bubin),
                                ('s_pummok', pummok),
                                ('s_sangi', '')
                             )
                    html_dict = extract_.extract(url, params)
                    if list_total_count % 10 > 1:
                        for i in range(len(html_dict['lists']['list'])):
                            dict3[f'{bubin}'].append({
                                'idx' : ((page -1) * 10) + (i + 1),
                                'PUMMOK' : html_dict['lists']['list'][i]['PUMMOK'],
                                'PUMJONG' : html_dict['lists']['list'][i]['PUMJONG'],
                                'UUN' : html_dict['lists']['list'][i]['UUN'],
                                'DDD' : html_dict['lists']['list'][i]['DDD'],
                                'PPRICE' : html_dict['lists']['list'][i]['PPRICE'],
                                'SSANGI' : html_dict['lists']['list'][i]['SSANGI'],
                                'CORP_NM' : html_dict['lists']['list'][i]['CORP_NM'],
                                'ADJ_DT' : html_dict['lists']['list'][i]['ADJ_DT']
                                })
                    elif list_total_count % 10 == 1:
                        if list_total_count > 1:
                            for i in range(10):
                                dict3[f'{bubin}'].append({
                                    'idx' : ((page -1) * 10) + (i + 1),
                                    'PUMMOK' : html_dict['lists']['list'][i]['PUMMOK'],
                                    'PUMJONG' : html_dict['lists']['list'][i]['PUMJONG'],
                                    'UUN' : html_dict['lists']['list'][i]['UUN'],
                                    'DDD' : html_dict['lists']['list'][i]['DDD'],
                                    'PPRICE' : html_dict['lists']['list'][i]['PPRICE'],
                                    'SSANGI' : html_dict['lists']['list'][i]['SSANGI'],
                                    'CORP_NM' : html_dict['lists']['list'][i]['CORP_NM'],
                                    'ADJ_DT' : html_dict['lists']['list'][i]['ADJ_DT']
                                    })
                            list_total_count -= 10
                        elif list_total_count == 1:
                            dict3[f'{bubin}'].append({
                                'idx' : int(html_dict['lists']['list_total_count']),
                                'PUMMOK' : html_dict['lists']['list']['PUMMOK'],
                                'PUMJONG' : html_dict['lists']['list']['PUMJONG'],
                                'UUN' : html_dict['lists']['list']['UUN'],
                                'DDD' : html_dict['lists']['list']['DDD'],
                                'PPRICE' : html_dict['lists']['list']['PPRICE'],
                                'SSANGI' : html_dict['lists']['list']['SSANGI'],
                                'CORP_NM' : html_dict['lists']['list']['CORP_NM'],
                                'ADJ_DT' : html_dict['lists']['list']['ADJ_DT']
                                })
                dict2[f'{pummok}'].append(dict3)
            else:
                pass
        dict1['data'].append(dict2)
    return dict1

def SG_partitioning(data):
        import gzip
        import json

        if len(data['data']) != 0:
            year = data['data'][0]['감귤'][0]['11000101'][0]['ADJ_DT'][0:4]
            month = data['data'][0]['감귤'][0]['11000101'][0]['ADJ_DT'][4:6]
            date = data['data'][0]['감귤'][0]['11000101'][0]['ADJ_DT']

        directory = f'{year}/{month}/{date}.json.gz'

        return data, directory

def etl_pipeline(date):
    data = transform(date)
    load_.s3_load(data, AWS_SERVICE_NAME, REGION, AWS_ACCESS_ID, AWS_SECRET_KEY, AWS_BUCKET_NAME, SG_partitioning)

etl_pipeline('20230407')
# json 원본파일 14mb
# gzip 압축파일 181kb

end = time.time()
print(f"{end - start:.2f} sec")
# 분산처리 전 346.23초 소요