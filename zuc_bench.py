import datetime
import secrets

import bench
import zuc
import zuc_optimized

REPEAT_COUNT = 20
BYTE_LENGTH = 20

_key_length = 128 // 8
_iv_length = 128 // 8

m = secrets.token_bytes(BYTE_LENGTH)
k = secrets.token_bytes(_key_length)
iv = secrets.token_bytes(_iv_length)

bench.bench_output([zuc.encrypt, zuc_optimized.encrypt], [k, iv, m], REPEAT_COUNT)
