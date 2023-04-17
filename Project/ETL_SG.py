from Core import Core

class ETL_SG(Core):
    """
    SG sub_project etl pipeline
    """
    def __init__(self, env=None):
        super().__init__(env)
    
    def _extract_data(self, date):
        """
        특수한 경우,
        여러번의 _extract_url 함수 호출로 전체 데이터를 추출
        """
        import os
        import math
        import json
        import pandas as pd
        from dotenv import load_dotenv
        load_dotenv()

        def extract_url(url, param = None):
            import cp2_modules.extract_ as ext

            return ext.extract(url, param)

        API_ID = os.getenv('garak_id')
        API_PW = os.getenv('garak_passwd')
        URL = 'http://www.garak.co.kr/publicdata/dataOpen.do?'

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
                        ('id', API_ID),
                        ('passwd', API_PW),
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
                list_total_count = int(extract_url(URL, params)['lists']['list_total_count'])
                total_page = math.ceil(int(list_total_count) / 10)

                if int(list_total_count) != 0:
                    for page in range(1, total_page+1):
                        params = (
                                    ('id', API_ID),
                                    ('passwd', API_PW),
                                    ('dataid', 'data12'),
                                    ('pagesize', '10'),
                                    ('pageidx', page),
                                    ('portal.templet', 'false'),
                                    ('s_date', date),
                                    ('s_bubin', bubin),
                                    ('s_pummok', pummok),
                                    ('s_sangi', '')
                                )
                        html_dict = extract_url(URL, params)
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

        flattened_data = []
        for item_data in dict1['data']:
            for item, bubin_list in item_data.items():
                for bubin_data in bubin_list:
                    for bubin, transactions in bubin_data.items():
                        for transaction in transactions:
                            flattened_row = transaction.copy()
                            flattened_row['item'] = item
                            flattened_row['bubin'] = bubin
                            flattened_data.append(flattened_row)

        return flattened_data
    
    def _load_data(self, data, aws_service_name, region, aws_access_id, aws_secret_key, aws_bucket_name, partitioning_func = None):
        """
        Spark 를 이용한 데이터 처리 및 분석 가능
        (DataFrame 형태로 반환)
        """
        import cp2_modules.load_ as aws

        aws.s3_load(data, aws_service_name, region, aws_access_id, aws_secret_key, aws_bucket_name, partitioning_func = None)