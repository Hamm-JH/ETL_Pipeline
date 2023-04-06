
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

#region [compress_]

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

#endregion [compress_]

def compress(data, method='zlib'):
    """ 데이터를 압축하는 함수 """
    return handle_compress[method](data)

def compress_test(data, method='zlib'):
    """ 데이터를 압축하는 함수 """
    print('기존 데이터 사이즈:', len(data))
    compressed = compress(data, method)
    print('압축 결과 사이즈:', len(compressed))
    print('압축률:', len(compressed) / len(data) * 100, '%')
    print('압축 방식:', method)
    print('압축 결과:', compressed)
    # print('압축 해제 결과:', handle_decompress[compress](compressed))

def decompress(data, method='zlib'):
    """ 데이터를 압축해제하는 함수 """
    return handle_decompress[method](data).decode()

def decompress_test(data, method='zlib'):
    """ 데이터를 압축해제하는 함수 """
    print('압축 데이터 사이즈:', len(data))
    decompressed = decompress(data, method)
    print('압축 해제 결과 사이즈:', len(decompressed))
    print('압축 해제율:', len(decompressed) / len(data) * 100, '%')
    print('압축 해제 방식:', method)
    print('압축 해제 결과:', decompress(data, method))



# def compress_file(file_path, compress='zlib'):
#     """ 파일을 압축하는 함수 """
#     with open(file_path, 'rb') as f:
#         data = f.read()
#     compressed = compress(data, compress)
#     with open(file_path + '.compress', 'wb') as f:
#         f.write(compressed)