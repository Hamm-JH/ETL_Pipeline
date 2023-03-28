'''
dacon 페이지에 올라온 농넷 API 코드는 현재 연결 안됨

AT 도매시장 통합홈페이지 = https://at.agromarket.kr/index.do
농산물유통정보 = https://www.kamis.or.kr/customer/main/main.do
서울시농수산식품공사 = https://www.garak.co.kr/main/main.do

실시간 경락정보를 받을 수 있는 API로 대체
'''

import urllib.request
import json
import datetime

today = datetime.datetime.today()
yesterday = (today - datetime.timedelta(1)).strftime('%Y%m%d')
url = 'https://www.nongnet.or.kr/api/whlslDstrQr.do?sdate='

response = urllib.request.urlopen(url+yesterday).read()
data = json.loads(response)

print(data)
# 현재는 이용불가