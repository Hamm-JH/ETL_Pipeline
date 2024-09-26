
print('this is modules/json_ __init__.py')

# TODO : json 모듈에 관련해서 추가할만한 함수 생각해보기

def str_to_json(str):
    """ 문자열을 json으로 변환하는 함수 """
    import json

    return json.loads(str.replace("'", "\""))

def dump_data(data):
    """ 데이터를 파일로 저장하는 함수 """
    import json

    return json.dumps(data)
