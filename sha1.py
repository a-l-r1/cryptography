import functools
import operator
from typing import Iterable

import hash_common

_h = (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0)
_iv = bytes.join(b'', map(lambda x: int.to_bytes(x, 4, 'big'), _h))
_block_length = 512
_message_length_desc_length = 64

_w_entry_length = 32
_w_extended_start_index = 16
_w_extended_end_index = 79

_f_result_length = 160
_f_intermediate_result_part_length = 32
_f_rounds = 80

_k = (0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xca62c1d6)


def _pad(m: bytes) -> bytes:
    m_length = len(m)
    result = m

    result += bytes((0x80,))

    # TODO: just calculate this
    byte_gap_length = 0
    while (m_length + 1 + byte_gap_length) % (_block_length // 8) != 448 // 8:
        byte_gap_length += 1
    result += bytes(byte_gap_length)

    result += (m_length * 8).to_bytes(_message_length_desc_length // 8, 'big')

    return result


def _4_byte_left_rotate(b: bytes) -> bytes:
    # get the MSB
    msb = (b[0] & 0x80) >> 7

    result = (((int.from_bytes(b, 'big') << 1) & 0xffffffff) | msb).to_bytes(4, 'big')
    return result


def _32_bit_int_left_rotate(n: int, bit_count: int) -> int:
    return ((n << bit_count) | (n >> (32 - bit_count))) & 0xffffffff


def _bytes_and(a: bytes, b: bytes) -> bytes:
    return bytes(x & y for x, y in zip(a, b))


def _bytes_or(a: bytes, b: bytes) -> bytes:
    return bytes(x | y for x, y in zip(a, b))


def _bytes_not(a: bytes) -> bytes:
    return bytes(~x for x in a)


def _bytes_xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def _32_bit_int_add_no_overflow(a: int, b: int):
    return (a + b) & 0xffffffff


def _pad_and_iter_chunks(m: bytes) -> Iterable[bytes]:
    m = _pad(m)
    return (m[i:i + _block_length // 8] for i in range(0, len(m), _block_length // 8))


def _f(block: bytes, last_result: bytes) -> bytes:
    w = [int.from_bytes(block[i: i + _w_entry_length // 8], 'big') for i in range(0, len(block), _w_entry_length // 8)]

    for i in range(_w_extended_start_index, _w_extended_end_index + 1):
        w.append(_32_bit_int_left_rotate(functools.reduce(operator.xor, (w[i - 3], w[i - 8], w[i - 14], w[i - 16])), 1))

    a, b, c, d, e = map(lambda x: int.from_bytes(x, 'big'), (last_result[i: i + _f_intermediate_result_part_length // 8]
                        for i in range(0, _f_result_length // 8, _f_intermediate_result_part_length // 8)))
    a_orig, b_orig, c_orig, d_orig, e_orig = a, b, c, d, e

    for i in range(0, _f_rounds):
        f = 0
        k = 0

        if 0 <= i <= 19:
            f = (b & c) | (~b & d)
            k = _k[0]
        elif 20 <= i <= 39:
            f = b ^ c ^ d
            k = _k[1]
        elif 40 <= i <= 59:
            f = (b & c) | (b & d) | (c & d)
            k = _k[2]
        elif 60 <= i <= 79:
            f = b ^ c ^ d
            k = _k[3]

        tmp = (_32_bit_int_left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff
        e = d
        d = c
        c = _32_bit_int_left_rotate(b, 30)
        b = a
        a = tmp

    return bytes.join(b'', map(lambda x, y: int.to_bytes((x + y) & 0xffffffff, 4, 'big'),
                               (a, b, c, d, e), (a_orig, b_orig, c_orig, d_orig, e_orig)))


def digest(m: bytes) -> bytes:
    return hash_common.merkle_damgard_wide_pipe(_iv, _pad_and_iter_chunks(m), _f,
                                                _block_length // 8, _f_result_length // 8)


def hmac(m: bytes, k: bytes) -> bytes:
    return hash_common.hmac(m, k, digest, _block_length // 8)
