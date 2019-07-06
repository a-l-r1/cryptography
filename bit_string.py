from typing import List

ord_0 = ord('0')
ord_1 = ord('1')
encoding_ascii = 'ascii'

_bin_str_actual_start_index = 2


class BitString(str):
    def __init__(self, *args):
        super(BitString, self).__init__()

    def __add__(self, other):
        return BitString(super(BitString, self).__add__(other))

    def __getitem__(self, item):
        return BitString(super(BitString, self).__getitem__(item))

    def __xor__(self, other):
        length = len(self)

        if length != len(other):
            raise ValueError("xor: BitString not of equal length")

        result = bytearray(length)

        for i in range(length):
            if self[i] == other[i]:
                result[i] = ord_0
            else:
                result[i] = ord_1

        return BitString(result.decode(encoding_ascii))


all_bits = (BitString('0'), BitString('1'))


def _int_to_8_bit(n: int) -> str:
    s = bytearray(8)

    for i in range(8):
        bitmask = 1 << i

        if n & bitmask == bitmask:
            s[8 - i - 1] = ord_1
        else:
            s[8 - i - 1] = ord_0

    return s.decode(encoding_ascii)


def _8_bit_to_int(s: str) -> int:
    result = 0

    for i in range(8):
        bitmask = 1 << i

        if s[8 - i - 1] == '1':
            result += bitmask
        elif s[8 - i - 1] == '0':
            pass

    return result


def bytes_to_bit_string(b: bytes) -> BitString:
    return BitString(''.join(map(_int_to_8_bit, b)))


def hex_to_bit_string(s: str) -> BitString:
    return bytes_to_bit_string(bytes.fromhex(s))


def bit_string_to_bytes(bs: BitString) -> bytes:
    if len(bs) % 8 != 0:
        raise ValueError("bit_string_to_bytes: len not multiple of 8")

    result_len = len(bs) // 8
    result = bytearray(result_len)

    for i in range(0, len(bs), 8):
        result[i // 8] = _8_bit_to_int(bs[i:i + 8])

    return bytes(result)


def small_int_to_bit_string(i: int, width: int = 8) -> BitString:
    if i < 0 or i >= (1 << width):
        raise ValueError("small_int_to_bit_string: i not in [0, %d]" % (2 ** width))

    return BitString(bin(i)[_bin_str_actual_start_index:].rjust(width, '0'))


def bytearray_to_bit_string(ba: bytearray) -> BitString:
    return BitString(ba.decode(encoding_ascii))


def left_rshift(bs: BitString, n: int) -> BitString:
    if n > len(bs):
        raise ValueError("left_rshift: rotate length > string length")

    if n < 0:
        raise ValueError("left_rshift: rotate length < 0")

    return BitString(bs[n:] + bs[0:n])


def right_rshift(bs: BitString, n: int) -> BitString:
    length = len(bs)

    if n > length:
        raise ValueError("left_rshift: rotate length > string length")

    if n < 0:
        raise ValueError("left_rshift: rotate length < 0")

    return BitString(bs[length - n:] + bs[0:length - n])


def xor(a: BitString, b: BitString) -> BitString:
    return a ^ b


def switch_halves(bs: BitString) -> BitString:
    length = len(bs)

    if length % 2 != 0:
        raise ValueError("switch_halves: BitString length not even")

    l = bs[0:length // 2]
    r = bs[length // 2:]

    return BitString(r + l)


def permutation_by_table(bs: BitString, table: List[int]) -> BitString:
    result = bytearray(len(table))

    for i in range(len(table)):
        if bs[table[i] - 1] == '1':
            result[i] = ord_1
        else:
            result[i] = ord_0

    result = bytearray_to_bit_string(result)

    return result


def permutation_by_table_with_completion(bs: BitString, table: List[int]) -> BitString:
    result = bytearray(len(table))

    for i in range(len(table)):
        try:
            if bs[table[i] - 1] == '1':
                result[i] = ord_1
            else:
                result[i] = ord_0
        except IndexError:
            result[i] = ord_0

    result = bytearray_to_bit_string(result)

    return result
