
# 테스트 데이터 작성

# 압축 모듈별로 압축 진행

# 압축 결과 저장

# import gzip

# with open("test.gz", "wb") as f:
#     f.write(gzip.compress(testdata_txt.encode()))

# 압축 결과 비교

def save_single_string_to_file(filename, string):
    with open(filename, "w") as f:
        f.write(string)

empty_string = ""
save_single_string_to_file("./Work_JH/test/empty.txt", empty_string)

txt = "A" * 1000000
save_single_string_to_file("./Work_JH/test/txt_A.txt", txt)

txt2 = "가" * 1000000
save_single_string_to_file("./Work_JH/test/txt_가.txt", txt2)

txt3 = "A" * 500000 + "B" * 500000
save_single_string_to_file("./Work_JH/test/txt_AB.txt", txt3)

txt4 = "A" * 500000 + "가" * 500000
save_single_string_to_file("./Work_JH/test/txt_A가.txt", txt4)

def save_single_byte_to_file(filename, byte):
    with open(filename, "wb") as f:
        f.write(byte)

byte1 = txt.encode()
save_single_byte_to_file("./Work_JH/test/byte_A.txt", byte1)

byte2 = txt2.encode()
save_single_byte_to_file("./Work_JH/test/byte_가.txt", byte2)

byte3 = txt3.encode()
save_single_byte_to_file("./Work_JH/test/byte_AB.txt", byte3)

byte4 = txt4.encode()
save_single_byte_to_file("./Work_JH/test/byte_A가.txt", byte4)

import gzip

zip1 = gzip.compress(byte1)
save_single_byte_to_file("./Work_JH/test/zip_A_", zip1)

# with open("./Work_JH/test/byte_A.txt", "rb") as f:
#     print(len(f.read()))