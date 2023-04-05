import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from modules.compress_ import _compress, _decompress, compress, decompress
_compress()
_decompress()

data = 'test' * 1000
method = 'zlib'
print('기존 데이터 사이즈:', len(data))

# 압축
compressed = compress(data, method)
print('압축 결과 사이즈:', len(compressed))
print('압축비 (압축사이즈) / (압축 전 사이즈):', len(compressed) / len(data))
print('압축 방식:', method)
print('압축 데이터:', compressed)
