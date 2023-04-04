'''
dacon 페이지에 올라온 농넷 API 코드는 현재 연결 안됨

서울시농수산식품공사 = https://www.garak.co.kr/main/main.do

실시간 경락정보를 받을 수 있는 API로 대체
'''

import requests
import os
import json
import xmltodict
from dotenv import load_dotenv
load_dotenv()

# def get_page(s_date, s_bubin, s_pummok):
#     '''
#     api 데이터 호출 함수
#     '''
#     garak_id = os.environ.get('garak_id')
#     garak_passwd = os.environ.get('garak_passwd')

#     url = f'http://www.garak.co.kr/publicdata/dataOpen.do?\
#         id={garak_id}&passwd={garak_passwd}&dataid=data12&pagesize=10\
#         &pageidx=1&portal.templet=false&s_date={s_date}\
#         &s_bubin={s_bubin}&s_pummok={s_pummok}&s_sangi='
#     page = requests.get(url)
#     html = page.text
#     return html

# print(get_page(20230327, 11000101, '사과'))

url = 'http://www.garak.co.kr/publicdata/dataOpen.do?id=3392&passwd=tmcltmcl547!&dataid=data12&pagesize=10&pageidx=1&portal.templet=false&s_date=20191030&s_bubin=11000101&s_pummok=사과&s_sangi='

page = requests.get(url)
html = page.text

html_dict = xmltodict.parse(html)
json_object = json.dumps(html_dict, ensure_ascii=False)

print(json_object)