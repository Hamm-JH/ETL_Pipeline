
print('this is modules/b64uuid_ __init__.py')

def encode_b64uuid_64(b64uuid):
    """ b64uuid를 uuid로 변환하는 함수 """
    from b64uuid import B64UUID

    start32 = B64UUID(b64uuid[:32])
    end32 = B64UUID(b64uuid[32:])

    return start32.string + end32.string

def decode_b64uuid_64(uuid):
    """ uuid -> b64uuid """
    pass