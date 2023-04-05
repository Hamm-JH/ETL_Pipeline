import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from modules.compress_ import _compress, _decompress, compress, decompress, compress_test, decompress_test
_compress()
_decompress()

data = 'test' * 1000
method = 'zlib'

# 압축
compressed = compress(data, method)

compress_test(data, method)
decompress_test(compressed, method)
