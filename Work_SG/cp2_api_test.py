'''
dacon 페이지에 올라온 농넷 API 코드는 현재 연결 안됨

AT 도매시장 통합홈페이지 = https://at.agromarket.kr/index.do
농산물유통정보 = https://www.kamis.or.kr/customer/main/main.do
서울시농수산식품공사 = https://www.garak.co.kr/main/main.do

실시간 경락정보를 받을 수 있는 API로 대체
'''

import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

def get_page(s_date, s_bubin, s_pummok, s_sangi):
    '''
    api 데이터 호출 함수
    '''
    garak_id = os.environ.get('garak_id')
    garak_passwd = os.environ.get('garak_passwd')

    url = f'http://www.garak.co.kr/publicdata/dataOpen.do?\
        id={garak_id}&passwd={garak_passwd}&dataid=data12&pagesize=10\
        &pageidx=1&portal.templet=false&s_date={s_date}\
        &s_bubin={s_bubin}&s_pummok={s_pummok}&s_sangi={s_sangi}'
    page = requests.get(url)
    parsed_data = json.loads(page.text)
    return page.text

print(get_page(20230327, 11000101, '사과', ''))
# 오류 발생 해결중