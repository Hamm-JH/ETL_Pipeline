from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(f"대칭키:{key}"); print()

fernet = Fernet(key)
json_log = {"url": "/api/products/product/24", "method": "DELETE", "product_id": 24, "user_id": 21, "name": "log_file2", "inDate": "2022-12-01T01:32:21.437Z", "detail": {"message": "DELETE access Board Detail", "levelname": "INFO"}}
encrypt_str = fernet.encrypt(f"{json_log}".encode('ascii'))
print("암호화된 문자열:", encrypt_str); print()

decrypt_str = fernet.decrypt(encrypt_str)
print("복호화된 문자열: ", decrypt_str)