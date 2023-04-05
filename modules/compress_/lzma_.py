
def compress_test():
    print('lzma compress test')

def decompress_test():
    print('lzma decompress test')

def compress(data):
    """ 데이터를 압축하는 함수 """
    if type(data) == str:
        data = data.encode()
        
    import lzma
    return lzma.compress(data)

def decompress(data):
    """ 데이터를 압축해제하는 함수 """
    import lzma
    return lzma.decompress(data)