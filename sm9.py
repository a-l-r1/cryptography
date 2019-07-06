import math
import secrets
from typing import Tuple

import gcd
import sm3
import sm9_common
from ec import EC, ECPoint


def kgc_init() -> Tuple[int, ECPoint, bytes]:
    # [1, n - 1] -> [0, n - 2] -> [0, n - 1)
    ke = secrets.randbelow(sm9_common.n_t - 1)
    ke += 1

    p_pub_e = ke * sm9_common.p_1

    return ke, p_pub_e, sm9_common.hid


def _int_ceil(dividend: int, divisor: int) -> int:
    if dividend % divisor == 0:
        return dividend // divisor
    else:
        return dividend // divisor + 1

def _int_floor(dividend: int, divisor: int) -> int:
    return dividend // divisor


def _h_with_prefix(m: bytes, n: int, prefix: bytes) -> int:
    ct = 1
    h_len = 8 * math.ceil(5 * math.log2(sm9_common.n) / 32)
    # SM3
    v = 256

    h_a = [b'']

    for i in range(1, _int_ceil(h_len, v)):
        h_a.append(sm3.digest(prefix + m + ct.to_bytes(4, 'big')))

    if h_len % v != 0:
        h_a[-1] = h_a[-1][(h_len - v * _int_floor(h_len, v)) // 8]

    h_a_all = bytes().join(h_a)

    h_1 = int.from_bytes(h_a_all, 'big')
    h_1 = (h_1 % (n - 1)) + 1

    return h_1


def _h1(m: bytes, n: int) -> int:
    return _h_with_prefix(m, n, bytes((0x01,)))


def _h2(m: bytes, n: int) -> int:
    return _h_with_prefix(m, n, bytes((0x02,)))


def _kdf(z: bytes, k_len: int) -> bytes:
    if k_len % 8 != 0:
        raise ValueError("_kgf(): unsupported key length")

    ct = 1
    v = 256

    # make indices match the spec
    h_a = [b'']

    for i in range(1, _int_ceil(k_len, v) + 1):
        h_a.append(sm3.digest(z + int.to_bytes(ct, 32 // 8, 'big')))
        ct += 1

    if k_len % v != 0:
        h_a[_int_ceil(k_len, v)] = h_a[_int_ceil(k_len, v)][:(k_len - (v * (k_len // v))) // 8]

    return bytes.join(bytes(), h_a)


def kgc_gen_user_pk(id_: bytes, kgc_sk: int, kgc_hid: bytes) -> ECPoint:
    ke = kgc_sk
    t_1 = (_h1(id_ + kgc_hid, sm9_common.n) + ke) % sm9_common.n

    if t_1 == 0:
        raise ValueError("kgc_gen_pk(): t_1 == 0, key regeneration needed")

    t_2 = ke * gcd.get_modular_inverse(t_1, sm9_common.n)

    de = t_2 * sm9_common.p_2
    return de
