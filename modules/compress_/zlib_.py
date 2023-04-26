
def compress_test():
    print('zlib compress test')

def decompress_test():
    print('zlib decompress test')

def compress(data):
    """ 데이터를 압축하는 함수 """
    # print(type(data))
    if type(data) == str:
        data = data.encode()

    import zlib
    return zlib.compress(data)

def decompress(data):
    """ 데이터를 압축해제하는 함수 """
    import zlib
    return zlib.decompress(data)