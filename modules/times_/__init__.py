
print("this is modules/times_ __init__.py")

# TODO : datetime 모듈과 연결성 나중에 생각해보기

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