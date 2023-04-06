
print('this is modules/cryptography_ __init__.py')

# TODO : 키 생성 함수 필요

def encrypt(key, data):
    """ 대칭키와 암호화할 데이터를 받아서 암호화된 데이터를 반환하는 함수 """
    from cryptography.fernet import Fernet

    _fernet = Fernet(key)

    return _fernet.encrypt(data)

def decrypt(key, data):
    """ 대칭키와 암호화된 데이터를 받아서 복호화된 데이터를 반환하는 함수 """
    from cryptography.fernet import Fernet

    _fernet = Fernet(key)

    return _fernet.decrypt(data)