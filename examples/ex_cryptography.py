from cryptography.fernet import Fernet

# 대칭키 생성
key = Fernet.generate_key()
print(f"대칭키:{key}"); print()

# 대칭키를 이용한 암호화 인스턴스 생성
fernet = Fernet(key)

# 암호화할 문자열
json_log = {"url": "/api/products/product/24", "method": "DELETE", "product_id": 24, "user_id": 21, "name": "log_file2", "inDate": "2022-12-01T01:32:21.437Z", "detail": {"message": "DELETE access Board Detail", "levelname": "INFO"}}

# 문자열을 바이트로 변환
encrypt_str = fernet.encrypt(f"{json_log}".encode('ascii'))
print("암호화된 문자열:", encrypt_str); print()

# 바이트를 문자열로 변환
decrypt_str = fernet.decrypt(encrypt_str)
print("복호화된 문자열: ", decrypt_str)