import datetime

# # String 값을 datetime object로 변경하는 방법 :: 에러 발생, 추후 점검 필요
# date_string = '2015-07-23 18:59:09'
# datetime.datetime.strptime('date_string', '%Y-%m-%d %H:%M:%S')

# timestamp to datetime
timestamp = 1463460958000
datetimeobj = datetime.datetime.fromtimestamp(timestamp/1000)
print(datetimeobj)
print(type(datetimeobj))
print()

# datetime to timestamp
import time
timestamp = time.mktime(datetimeobj.timetuple())
print(timestamp)
print(type(timestamp))
print()