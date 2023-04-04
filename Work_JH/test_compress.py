
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

def save_single_byte_to_file(filename, byte):
    with open(filename, "wb") as f:
        f.write(byte)

empty_string = ""
txt = "A" * 1000000
txt2 = "가" * 1000000
txt3 = "A" * 500000 + "B" * 500000
txt4 = "A" * 500000 + "가" * 500000

# txt = "A" * 5

byte1 = txt.encode()
byte2 = txt2.encode()
byte3 = txt3.encode()
byte4 = txt4.encode()

def save_texts():
    save_single_string_to_file("./Work_JH/test/empty.txt", empty_string)
    save_single_string_to_file("./Work_JH/test/txt_A.txt", txt)
    save_single_string_to_file("./Work_JH/test/txt_가.txt", txt2)
    save_single_string_to_file("./Work_JH/test/txt_AB.txt", txt3)
    save_single_string_to_file("./Work_JH/test/txt_A가.txt", txt4)

    save_single_byte_to_file("./Work_JH/test/byte_A.txt", byte1)
    save_single_byte_to_file("./Work_JH/test/byte_가.txt", byte2)
    save_single_byte_to_file("./Work_JH/test/byte_AB.txt", byte3)
    save_single_byte_to_file("./Work_JH/test/byte_A가.txt", byte4)

# save_texts()

import gzip

zip1 = gzip.compress(byte1)
save_single_byte_to_file("./Work_JH/test/zip_A", zip1)

zip11 = gzip.compress(byte1)
save_single_byte_to_file("./Work_JH/test/zip_A.txt", zip11)

zip12 = gzip.compress(byte1)
save_single_byte_to_file("./Work_JH/test/zip_A.zip", zip12)


zip2 = gzip.compress(byte1)
save_single_byte_to_file("./Work_JH/test/zip_A2.zip", zip2)

zip21 = gzip.compress(byte1)
save_single_byte_to_file("./Work_JH/test/zip_A2.gz", zip21)

zip22 = gzip.compress(byte1)
save_single_byte_to_file("./Work_JH/test/zip_A2.tar", zip22)


zip3 = gzip.compress(byte1)
save_single_byte_to_file("./Work_JH/test/zip_A3.zip", zip3)

import bz2
bz1 = bz2.compress(byte1)
save_single_byte_to_file("./Work_JH/test/bz_A.bz2", bz1)

import lzma
lz1 = lzma.compress(byte1)
save_single_byte_to_file("./Work_JH/test/lz_A.lzma", lz1)