
print('this is modules/compress_ __init__.py')

# TODO : json 모듈과 연결성 나중에 생각해보기
def _json_dump_data(data):
    """ 데이터를 파일로 저장하는 함수 """
    import json

    return json.dumps(data)

"""
TODO : 데이터 압축 모듈별로 압축함수 구현하기
"""
def compress_data(str_data):
    """ 데이터를 압축하는 함수 """
    import zlib
    return zlib.compress(str_data.encode())

    # import gzip
    # return gzip.compress(str_data.encode())

"""
TODO : 데이터 압축 해제 모듈별로 압축해제함수 구현하기
"""
def compress_dict(dict_data):
    """ dict 데이터를 압축하는 함수 """
    return compress_data(_json_dump_data(dict_data))

def compress():
    """ 데이터 압축 """
    import compress_.zlib_ as zlib_
    
    print('hello')
    zlib_.compress_test()

def decompress():
    """ 데이터 압축 해제 """
    import compress_.zlib_ as zlib_
    print('hello')
    zlib_.decompress_test()
