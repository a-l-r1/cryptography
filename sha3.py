import hashlib
import itertools
from typing import List, Sequence, Tuple, Union

import hash_common


_l = 6
_w = 2 ** _l


class _KeccakState(object):
    _rc_table = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
        0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
        0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
        0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
        0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
        0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
    ]
    """
    _rc_table = list(map(
        lambda x: bytes(reversed(bytes.fromhex(hex(x)[2:].rjust(_w // 4, '0')))),
        _rc_table))
    """

    _r_table = [
        [0, 36, 3, 41, 18],
        [1, 44, 10, 45, 2],
        [62, 6, 43, 15, 61],
        [28, 55, 25, 21, 56],
        [27, 20, 39, 8, 14]
    ]

    _l = 6
    _w = 2 ** 6
    _bytearray_length = 5 * 5 * _w // 8

    def __init__(self: "_KeccakState") -> None:
        self.data = bytearray(self._bytearray_length)

    def load(self: "_KeccakState", b: Sequence[int]) -> None:
        if len(self.data) > self._bytearray_length:
            raise ValueError("load(): byte sequence too long")

        for i in range(len(b)):
            self.data[i] ^= b[i]

    def __getitem__(self: "_KeccakState", item: Union[int, Tuple, slice]) -> int:
        if not isinstance(item, Tuple):
            raise ValueError("__getitem__(): not implemented")

        if len(item) == 3:
            x, y, z = item

            # column major
            bit_index = _w * (5 * y + x) + z

            index = bit_index // 8
            bitmask = 1 << (7 - (bit_index % 8))

            if self.data[index] & bitmask == bitmask:
                return 1
            else:
                return 0

        raise ValueError("__getitem__(): not implemented")

    def __setitem__(self, key: Union[int, Tuple, slice], value: int) -> None:
        if not isinstance(key, Tuple):
            raise ValueError("__setitem__(): not implemented")

        if not isinstance(value, int):
            raise ValueError("__setitem__(): not implemented on such values")

        if value not in (0, 1):
            raise ValueError("__setitem__(): invalid value")

        if len(key) == 3:
            x, y, z = key

            # column major
            bit_index = _w * (5 * y + x) + z

            index = bit_index // 8
            bitmask = 1 << (7 - (bit_index % 8))

            if value == 1:
                self.data[index] |= bitmask
            else:
                self.data[index] &= 0xff ^ bitmask

            return

        raise ValueError("__setitem__(): not implemented")

    @staticmethod
    def _64_bit_int_hex(x: int) -> str:
        return hex(x)[2:].rjust(64 // 4, '0')

    def _get_lane(self: "_KeccakState", i: int, j: int) -> int:
        result = 0

        for k in range(_w):
            result |= self[i, j, k] << (63 - k)

        return result

    def __str__(self) -> str:
        result = ''

        result += '_KeccakState(\n'

        # column major
        for i in range(5):
            for j in range(5):
                result += '(%d, %d): ' % (i, j)
                result += self._64_bit_int_hex(self._get_lane(i, j))
                result += ' '
            result += '\n'

        result += ')'

        return result

    def theta(self: "_KeccakState") -> "_KeccakState":
        result = _KeccakState()

        c = [[0 for _ in range(_w)] for __ in range(5)]
        d = [[0 for _ in range(_w)] for __ in range(5)]

        for x, z in itertools.product(range(5), range(_w)):
            c[x][z] = self[x, 0, z] ^ self[x, 1, z] ^ self[x, 2, z] ^ \
                      self[x, 3, z] ^ self[x, 4, z]

        for x, z in itertools.product(range(5), range(_w)):
            d[x][z] = c[(x - 1) % 5][z] ^ c[(x + 1) % 5][(z + 1) % _w]

        for x, y, z in itertools.product(range(5), range(5), range(_w)):
            result[x, y, z] = self[x, y, z] ^ d[x][z]

        return result

    def rho(self: "_KeccakState") -> "_KeccakState":
        result = _KeccakState()

        for z in range(_w):
            result[0, 0, z] = self[0, 0, z]

        x, y = 1, 0

        for t in range(23 + 1):
            for z in range(_w):
                result[x, y, z] = self[x, y, (z + ((t + 1) * (t + 2) // 2)) % _w]

            x, y = y, (2 * x + 3 * y) % 5

        return result

    def pi(self: "_KeccakState") -> "_KeccakState":
        result = _KeccakState()

        for x, y, z in itertools.product(range(5), range(5), range(_w)):
            result[x, y, z] = self[(x + 3 * y) % 5, x, z]

        return result

    def chi(self: "_KeccakState") -> "_KeccakState":
        result = _KeccakState()

        for x, y, z in itertools.product(range(5), range(5), range(_w)):
            result[x, y, z] = self[x, y, z] ^ ((self[(x + 1) % 5, y, z] ^ 1) &
                                               self[(x + 2) % 5, y, z])

        return result

    def iota(self: "_KeccakState", round_: int) -> "_KeccakState":
        result = _KeccakState()

        result.data = self.data[:]

        for i in range(_w // 8):
            result.data[i] ^= self._rc_table[round_][i]

        return result

    @staticmethod
    def _rot(x: int, r: int):
        r %= _w
        return ((x << r) | (x >> (_w - r))) & 0xffffffffffffffff

    def f(self: "_KeccakState") -> "_KeccakState":
        lanes = [[0 for _ in range(5)] for __ in range(5)]

        for i, j in itertools.product(range(5), range(5)):
            # column major
            lanes[j][i] = int.from_bytes(self.data[8 * (i * 5 + j):8 * (i * 5 + j + 1)],
                                         'little')

        for round_ in range(24):
            # theta
            c = [lanes[x][0] ^ lanes[x][1] ^ lanes[x][2] ^ lanes[x][3] ^ lanes[x][4]
                 for x in range(5)]
            d = [c[(x - 1) % 5] ^ self._rot(c[(x + 1) % 5], 1) for x in range(5)]

            for x, y in itertools.product(range(5), range(5)):
                lanes[x][y] ^= d[x]

            # rho and pi
            b = [[0 for _ in range(5)] for __ in range(5)]

            for x, y in itertools.product(range(5), range(5)):
                b[y][(2 * x + 3 * y) % 5] = self._rot(lanes[x][y], self._r_table[x][y])

            # chi
            for x, y in itertools.product(range(5), range(5)):
                lanes[x][y] = b[x][y] ^ ((0xffffffffffffffff ^ b[(x + 1) % 5][y]) & b[(x + 2) % 5][y])

            # iota
            lanes[0][0] ^= self._rc_table[round_]

        result = _KeccakState()

        tmp_data = bytearray()
        for x, y in itertools.product(range(5), range(5)):
            # column major
            tmp_data += lanes[y][x].to_bytes(_w // 8, 'little')
        result.data = tmp_data

        return result


def _keccak(r: int, d: int, output_length: int, m: bytes) -> bytes:
    if d < 0 or d > 0xff:
        raise ValueError("_keccak(): invalid d")

    if r <= 0 or r >= 1600 or r % _w != 0:
        raise ValueError("_keccak(): invalid r")

    d = bytes((d,))

    p = bytearray(m + d)
    p_target_length = len(p)

    block_size = r // 8

    if p_target_length % block_size == 0:
        pass
    else:
        p_target_length += block_size - (len(p) % block_size)

    p += bytearray(p_target_length - len(p))

    p[-1] ^= 0x80

    state = _KeccakState()

    # absorbing phase
    for block in [p[i:i + block_size] for i in range(0, p_target_length, block_size)]:
        state.load(block)
        state = state.f()

    # squeezing phase
    output_byte_length = output_length // 8

    z = bytes()
    while output_byte_length > 0:
        z += bytes(state.data)
        output_byte_length -= 5 * 5 * _w
        state = state.f()

    z = z[:output_length // 8]
    return z


def digest_224(m: bytes) -> bytes:
    return _keccak(1152, 0x06, 224, m)


def digest_256(m: bytes) -> bytes:
    return _keccak(1088, 0x06, 256, m)


def digest_384(m: bytes) -> bytes:
    return _keccak(832, 0x06, 384, m)


def digest_512(m: bytes) -> bytes:
    return _keccak(576, 0x06, 512, m)


digest = digest_256


def hmac_224(m: bytes, k: bytes) -> bytes:
    return hash_common.hmac(m, k, digest_224, 144)


def hmac_256(m: bytes, k: bytes) -> bytes:
    return hash_common.hmac(m, k, digest_256, 136)


def hmac_384(m: bytes, k: bytes) -> bytes:
    return hash_common.hmac(m, k, digest_384, 104)


def hmac_512(m: bytes, k: bytes) -> bytes:
    return hash_common.hmac(m, k, digest_512, 72)


hmac = hmac_256
