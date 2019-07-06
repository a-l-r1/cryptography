import secrets
from typing import Tuple

import cipher_common
import gcd
from sm2_common import *

# inferred from sm2_common.n
_pt_chunk_length = 31
_ct_chunk_length = 96
_byte_int_conversion_endian = 'big'

_p = 265371653
_g = 2


def gen_key() -> Tuple[fp, ECPoint]:
    # [0, n - 1) -> [1, n)
    x = secrets.randbelow(n - 1)
    x = x + 1

    x = fp(x)

    return x, x * g


def encrypt(p_: int, pk: ECPoint) -> Tuple[ECPoint, int]:
    if p_ >= n or p_ < 0:
        raise ValueError("encrypt: invalid m")

    while True:
        # (0, n) -> [0, n - 1)
        k = secrets.randbelow(n - 1)
        k += 1

        x_1 = k * g
        x_2 = k * pk

        if x_2.x == x_2.x.__class__(0):
            continue

        c_int = (p_ * x_2.x.data) % n

        return x_1, c_int


def decrypt(c: Tuple[ECPoint, int], sk: fp) -> int:
    x_1 = c[0]
    c_int = c[1]

    if c_int >= n or c_int < 0:
        raise ValueError("decrypt: invalid actual c")

    x_2 = sk * x_1

    m = (c_int * gcd.get_modular_inverse(x_2.x.data, n)) % n
    return m


def _encrypt_chunk(pt_chunk: bytes, pk: fp, ct_chunk_length: int) -> bytes:
    p_ = int.from_bytes(pt_chunk, _byte_int_conversion_endian)
    c = encrypt(p_, pk)

    x_1 = c[0]
    c_int = c[1]

    # use + here will cause overflow
    result = x_1.x.data << (64 * 8) | x_1.y.data << (32 * 8) | c_int
    return int.to_bytes(result, ct_chunk_length, _byte_int_conversion_endian)


def _decrypt_chunk(ct_chunk: bytes, sk: ECPoint, pt_chunk_length: int) -> bytes:
    ct_huge_int = int.from_bytes(ct_chunk, _byte_int_conversion_endian)
    bitmask = (1 << 32 * 8) - 1

    c_int = ct_huge_int & bitmask
    ct_huge_int >>= 32 * 8
    y_data = ct_huge_int & bitmask
    ct_huge_int >>= 32 * 8
    x_data = ct_huge_int

    x_1 = ECPoint(ec, fp(x_data), fp(y_data))
    c = (x_1, c_int)

    p_ = decrypt(c, sk)

    try:
        return p_.to_bytes(pt_chunk_length, _byte_int_conversion_endian)
    except ValueError:
        raise ValueError("_decrypt_chunk: invalid ciphertext file")


def encrypt_file(pt_filename: str, ct_filename: str, pk: fp) -> None:
    cipher_common.encrypt_file(pt_filename, ct_filename, pk, _encrypt_chunk, _pt_chunk_length, _ct_chunk_length)


def decrypt_file(pt_filename: str, ct_filename: str, sk: Tuple[ECPoint]) -> None:
    cipher_common.decrypt_file(pt_filename, ct_filename, sk, _decrypt_chunk, _pt_chunk_length, _ct_chunk_length)
