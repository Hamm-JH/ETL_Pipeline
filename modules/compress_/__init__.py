
print('this is modules/compress_ __init__.py')

# TODO : json 모듈과 연결성 나중에 생각해보기
def _json_dump_data(data):
    """ 데이터를 파일로 저장하는 함수 """
    import json

    return json.dumps(data)

"""
[x] : 데이터 압축 모듈별로 압축함수 구현하기
"""
def compress_data(str_data):
    """ 데이터를 압축하는 함수 """
    import zlib
    return zlib.compress(str_data.encode())

    # import gzip
    # return gzip.compress(str_data.encode())

"""
[x] : 데이터 압축 해제 모듈별로 압축해제함수 구현하기
"""
def compress_dict(dict_data):
    """ dict 데이터를 압축하는 함수 """
    return compress_data(_json_dump_data(dict_data))

def _compress():
    """ 데이터 압축 """
    import compress_.zlib_ as zlib_
    
    print('hello')
    zlib_.compress_test()

def _decompress():
    """ 데이터 압축 해제 """
    import compress_.zlib_ as zlib_
    print('hello')
    zlib_.decompress_test()


def zlib_compress(data):
    """ zlib 데이터 압축 """
    import compress_.zlib_ as zlib_
    return zlib_.compress(data)

def zlib_decompress(data):
    """ zlib 데이터 압축 해제 """
    import compress_.zlib_ as zlib_
    return zlib_.decompress(data)

def gzip_compress(data):
    """ gzip 데이터 압축 """
    import compress_.gzip_ as gzip_
    return gzip_.compress(data)

def gzip_decompress(data):
    """ gzip 데이터 압축 해제 """
    import compress_.gzip_ as gzip_
    return gzip_.decompress(data)

def lzma_compress(data):
    """ lzma 데이터 압축 """
    import compress_.lzma_ as lzma_
    return lzma_.compress(data)

def lzma_decompress(data):
    """ lzma 데이터 압축 해제 """
    import compress_.lzma_ as lzma_
    return lzma_.decompress(data)

handle_compress = {
    'zlib': zlib_compress,
    'gzip': gzip_compress,
    'lzma': lzma_compress
}

handle_decompress = {
    'zlib': zlib_decompress,
    'gzip': gzip_decompress,
    'lzma': lzma_decompress
}

def compress(data, compress='zlib'):
    """ 데이터를 압축하는 함수 """
    return handle_compress[compress](data)

def decompress(data, compress='zlib'):
    """ 데이터를 압축해제하는 함수 """
    return handle_decompress[compress](data)
