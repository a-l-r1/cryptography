from typing import Iterable

import hash_common

_32_bit_mask = 0xffffffff

_iv = bytes.fromhex('7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e')

_block_length = 512
_result_length = 256
_message_length_desc_length = 64

_w_length = 132
_w_entry_length = 32
_w_extended_start_index = 16
_w_extended_middle_index = 67
_w_extended_end_index = 79


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


def _pad_and_iter_chunks(m: bytes) -> Iterable[bytes]:
    m = _pad(m)
    return (m[i:i + _block_length // 8] for i in range(0, len(m), _block_length // 8))


def _32_bit_int_left_rotate(n: int, bit_count: int) -> int:
    return ((n << bit_count) | (n >> (32 - bit_count))) & 0xffffffff


def _t(j: int) -> int:
    if 0 <= j <= 15:
        return 0x79cc4519
    if 16 <= j <= 63:
        return 0x7a879d8a


def _p0(x: int) -> int:
    return (x ^ _32_bit_int_left_rotate(x, 9) ^ _32_bit_int_left_rotate(x, 17)) & _32_bit_mask


def _p1(x: int) -> int:
    return (x ^ _32_bit_int_left_rotate(x, 15) ^ _32_bit_int_left_rotate(x, 23)) & _32_bit_mask


def _ff(j: int, x: int, y: int, z: int) -> int:
    if 0 <= j <= 15:
        return x ^ y ^ z
    if 16 <= j <= 63:
        return (x & y) | (x & z) | (y & z)


def _gg(j: int, x: int, y: int, z: int) -> int:
    if 0 <= j <= 15:
        return x ^ y ^ z
    if 16 <= j <= 63:
        return (x & y) | (~x & z)


def _f(block: bytes, last_result: bytes) -> bytes:
    w = [0 for _ in range(67 + 1)]

    for i in range(16):
        w[i] = int.from_bytes(block[i * _w_entry_length // 8:(i + 1) * _w_entry_length // 8], 'big')
    for i in range(16, 67 + 1):
        w[i] = _p1(w[i - 16] ^ w[i - 9] ^ _32_bit_int_left_rotate(w[i - 3], 15)) ^ \
               _32_bit_int_left_rotate(w[i - 13], 7) ^ w[i - 6]
    w_ = [w[j] ^ w[j + 4] for j in range(63 + 1)]

    a, b, c, d, e, f, g, h = map(lambda x: int.from_bytes(x, 'big'),
                                 (last_result[i * 4:(i + 1) * 4] for i in range(8)))

    for j in range(63 + 1):
        ss1 = _32_bit_int_left_rotate(
            (_32_bit_int_left_rotate(a, 12) + e + _32_bit_int_left_rotate(_t(j), j % 32)) & _32_bit_mask,
            7)
        ss2 = ss1 ^ _32_bit_int_left_rotate(a, 12)
        tt1 = (_ff(j, a, b, c) + d + ss2 + w_[j]) & _32_bit_mask
        tt2 = (_gg(j, e, f, g) + h + ss1 + w[j]) & _32_bit_mask

        d = c
        c = _32_bit_int_left_rotate(b, 9)
        b = a
        a = tt1
        h = g
        g = _32_bit_int_left_rotate(f, 19)
        f = e
        e = _p0(tt2)

    a, b, c, d, e, f, g, h = map(lambda x, y: int.from_bytes(x, 'big') ^ y,
                                 (last_result[i * 4:(i + 1) * 4] for i in range(8)), (a, b, c, d, e, f, g, h))

    return bytes.join(bytes(), map(lambda x: int.to_bytes(x, 4, 'big'), (a, b, c, d, e, f, g, h)))


def digest(m: bytes) -> bytes:
    return hash_common.merkle_damgard_wide_pipe(_iv, _pad_and_iter_chunks(m), _f,
                                                _block_length // 8, _result_length // 8)


def hmac(m: bytes, k: bytes) -> bytes:
    return hash_common.hmac(m, k, digest, _block_length // 8)
