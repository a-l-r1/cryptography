import itertools
import operator
from typing import List, Set

import bit_string
from bit_string import BitString
import feistel


des_orig_key_length = 64
_des_key_bitmask = ((1 << des_orig_key_length) - 1)
_des_actual_key_length = 56
_des_round_key_length = 48

_des_gen_key_pc_1_table = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

_des_gen_key_rounds = 16

_des_gen_key_shift_count_table = [
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
]

_des_gen_key_pc_2_table = [
    14, 17, 11, 24, 1, 5, 3, 28,
    15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32
]

des_block_length = 64
_des_round_count = 16

_des_ip_table = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

_des_e_output_length = 48

_des_e_table = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

_des_s_input_length = 48
_des_s_group_count = 8
_des_s_group_length = 6
_des_s_output_group_length = 4
_des_s_output_length = 32

_des_s_row_determination_bit_index_table = [
    0, 5
]

_des_s_row_determination_table = {
    BitString('00'): 0,
    BitString('01'): 1,
    BitString('10'): 2,
    BitString('11'): 3
}

_des_s_column_determination_bit_index_table = [
    1, 2, 3, 4
]

_des_s_column_determination_table = {
    BitString('0000'): 0,
    BitString('0001'): 1,
    BitString('0010'): 2,
    BitString('0011'): 3,
    BitString('0100'): 4,
    BitString('0101'): 5,
    BitString('0110'): 6,
    BitString('0111'): 7,
    BitString('1000'): 8,
    BitString('1001'): 9,
    BitString('1010'): 10,
    BitString('1011'): 11,
    BitString('1100'): 12,
    BitString('1101'): 13,
    BitString('1110'): 14,
    BitString('1111'): 15
}

_des_s_table = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 14, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

_des_p_input_length = 32

_des_p_table = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

_des_ip_inv_table = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]


_des_3round_round_count = 3

_des_p_inv_table = [
    9, 17, 23, 31, 13, 28, 2, 18,
    24, 16, 30, 6, 26, 20, 10, 1,
    8, 14, 25, 3, 4, 29, 11, 19,
    32, 12, 22, 7, 5, 27, 15, 21
]

_des_gen_key_pc_2_inv_table = [
    5, 24, 7, 16, 6, 10, 20, 18,
    49, 12, 3, 15, 23, 1, 9, 19,
    2, 50, 14, 22, 11, 51, 13, 4,
    52, 17, 21, 8, 47, 31, 27, 48,
    35, 41, 53, 46, 28, 54, 39, 32,
    25, 44, 55, 37, 34, 43, 29, 36,
    38, 45, 33, 26, 42, 56, 30, 40
]

_des_gen_key_pc_1_inv_table = [
    8, 16, 24, 56, 52, 44, 36, 57,
    7, 15, 23, 55, 51, 43, 35, 58,
    6, 14, 22, 54, 50, 42, 34, 59,
    5, 13, 21, 53, 49, 41, 33, 60,
    4, 12, 20, 28, 48, 40, 32, 61,
    3, 11, 19, 27, 47, 39, 31, 62,
    2, 10, 18, 26, 46, 38, 30, 63,
    1, 9, 17, 25, 45, 37, 29, 64
]


def _des_gen_key_pc_1(k: BitString) -> BitString:
    return bit_string.permutation_by_table(k, _des_gen_key_pc_1_table)


def _des_gen_key_pc_2(k: BitString) -> BitString:
    return bit_string.permutation_by_table(k, _des_gen_key_pc_2_table)


def _des_gen_key_list(k: bytes) -> List[BitString]:
    k_str = _des_gen_key_pc_1(bit_string.bytes_to_bit_string(k))
    c = k_str[0:_des_actual_key_length // 2]
    d = k_str[_des_actual_key_length // 2:]

    result = []

    for round_number in range(_des_gen_key_rounds):
        c = bit_string.left_rshift(c, _des_gen_key_shift_count_table[round_number])
        d = bit_string.left_rshift(d, _des_gen_key_shift_count_table[round_number])

        k = _des_gen_key_pc_2(BitString(c + d))
        result.append(k)

    return result


def _des_ip(p: BitString) -> BitString:
    return bit_string.permutation_by_table(p, _des_ip_table)


def _des_e(bs: BitString) -> BitString:
    return bit_string.permutation_by_table(bs, _des_e_table)


def _des_s_single_block(bs: BitString, group_number: int) -> BitString:
    curr_row = _des_s_row_determination_table[
        BitString(''.join(map(lambda x: bs[x], _des_s_row_determination_bit_index_table)))]
    curr_column = _des_s_column_determination_table[
        BitString(''.join(map(lambda x: bs[x], _des_s_column_determination_bit_index_table)))]
    curr_result_block = _des_s_table[group_number][curr_row][curr_column]

    return bit_string.small_int_to_bit_string(curr_result_block, _des_s_output_group_length)


def _des_s(bs: BitString) -> BitString:
    result_list = []

    for group_number in range(_des_s_group_count):
        curr_slice = bs[group_number * _des_s_group_length:group_number * _des_s_group_length + _des_s_group_length]
        curr_slice = BitString(curr_slice)

        result_list.append(_des_s_single_block(curr_slice, group_number))

    result = BitString(''.join(result_list))
    return result


def _des_p(bs: BitString) -> BitString:
    return bit_string.permutation_by_table(bs, _des_p_table)


def _des_ip_inv(bs: BitString) -> BitString:
    return bit_string.permutation_by_table(bs, _des_ip_inv_table)


def _des_f(bs: BitString, k: BitString) -> BitString:
    result = _des_e(bs)
    result = bit_string.xor(result, k)
    result = _des_s(result)
    result = _des_p(result)

    return result


def _des(bs: BitString, key_list: List[BitString]) -> BitString:
    result = _des_ip(bs)
    result = feistel.feistel_repetitive(result, key_list, _des_f, _des_round_count)
    result = bit_string.switch_halves(result)
    result = _des_ip_inv(result)

    return result


def _des_check(b: bytes, k: bytes) -> None:
    if len(b) != des_block_length // 8:
        raise ValueError("des_encrypt: p not of %d bits" % des_block_length)

    if len(k) != des_orig_key_length // 8:
        raise ValueError("des_encrypt: k not of %d bits" % des_orig_key_length)


def encrypt(p: bytes, k: bytes) -> bytes:
    _des_check(p, k)

    key_list = _des_gen_key_list(k)
    result = bit_string.bit_string_to_bytes(_des(bit_string.bytes_to_bit_string(p), key_list))

    return result


def decrypt(c: bytes, k: bytes) -> bytes:
    _des_check(c, k)

    key_list = _des_gen_key_list(k)
    key_list.reverse()
    result = bit_string.bit_string_to_bytes(_des(bit_string.bytes_to_bit_string(c), key_list))

    return result


def _des_3round(bs: BitString, key_list: List[BitString]) -> BitString:
    result = feistel.feistel_repetitive(bs, key_list, _des_f, _des_3round_round_count)

    return result


def des_3round_encrypt(p: bytes, k: bytes) -> bytes:
    _des_check(p, k)

    key_list = _des_gen_key_list(k)
    key_list = key_list[:_des_3round_round_count]
    result = bit_string.bit_string_to_bytes(_des_3round(bit_string.bytes_to_bit_string(p), key_list))

    return result


def des_3round_decrypt(p: bytes, k: bytes) -> bytes:
    _des_check(p, k)

    key_list = _des_gen_key_list(k)
    key_list = key_list[:_des_3round_round_count]
    key_list.reverse()
    result = bit_string.bit_string_to_bytes(_des_3round(bit_string.bytes_to_bit_string(p), key_list))

    return result


def _des_p_inv(bs: BitString) -> BitString:
    return bit_string.permutation_by_table(bs, _des_p_inv_table)


def _des_3round_cryptanalysis_differential_gen_test_set(e_1: BitString, e_2: BitString, c_diff: BitString,
                                                        group_number: int) -> Set[BitString]:
    e_diff = bit_string.xor(e_1, e_2)

    result = set()

    for b_int in range(1 << _des_s_group_length):
        b = bit_string.small_int_to_bit_string(b_int, _des_s_group_length)

        if bit_string.xor(_des_s_single_block(b, group_number),
                          _des_s_single_block(bit_string.xor(b, e_diff), group_number)) == c_diff:
            result.add(bit_string.xor(b, e_1))

    return result


def _des_3round_cryptanalysis_differential_two_pairs(p1: BitString, c1: BitString, p2: BitString,
                                                     c2: BitString) -> List[Set[BitString]]:
    mid = des_block_length // 2

    r_3_1 = BitString(c1[mid:])
    r_3_2 = BitString(c2[mid:])
    r_3_diff = bit_string.xor(r_3_1, r_3_2)

    l_0_1 = BitString(p1[:mid])
    l_0_2 = BitString(p2[:mid])
    l_0_diff = bit_string.xor(l_0_1, l_0_2)

    c_diff = _des_p_inv(bit_string.xor(r_3_diff, l_0_diff))

    l_3_1 = BitString(c1[:mid])
    l_3_2 = BitString(c2[:mid])
    e_1 = _des_e(l_3_1)
    e_2 = _des_e(l_3_2)

    c_diff_list = list(map(lambda x: BitString(c_diff[x:x + _des_s_output_group_length]),
                           range(0, des_block_length, _des_s_output_group_length)))
    e_1_list = list(map(lambda x: BitString(e_1[x:x + _des_s_group_length]),
                        range(0, _des_s_input_length, _des_s_group_length)))
    e_2_list = list(map(lambda x: BitString(e_2[x:x + _des_s_group_length]),
                        range(0, _des_s_input_length, _des_s_group_length)))

    result = []

    for i in range(_des_s_group_count):
        result.append(_des_3round_cryptanalysis_differential_gen_test_set(e_1_list[i], e_2_list[i],
                                                                          c_diff_list[i], i))

    return result


def _des_3round_cryptanalysis_differential_gen_possible_key_chunks(p_list: List[BitString],
                                                                   c_list: List[BitString]) -> List[Set[BitString]]:
    p_length = len(p_list)

    mid = des_block_length // 2

    occurrence_table = [
        {bit_string.small_int_to_bit_string(b, _des_s_group_length): 0 for b in range(1 << _des_s_group_length)}
        for _ in range(_des_s_group_count)]

    for i in range(0, p_length, 2):
        if p_list[i][mid:] != p_list[i + 1][mid:]:
            raise ValueError(__name__ + ": different R_0 in plaintext pair (%s, %s)" % (p_list[i], p_list[i + 1]))

        curr_p1, curr_c1, curr_p2, curr_c2 = p_list[i], c_list[i], p_list[i + 1], c_list[i + 1]
        curr_possible_keys = _des_3round_cryptanalysis_differential_two_pairs(curr_p1, curr_c1, curr_p2, curr_c2)

        for group_number in range(_des_s_group_count):
            for possible_key_chunk in curr_possible_keys[group_number]:
                occurrence_table[group_number][possible_key_chunk] += 1

    result = [set() for _ in range(_des_s_group_count)]

    for group_number in range(_des_s_group_count):
        result[group_number] = set(filter(lambda x: occurrence_table[group_number][x] == p_length // 2,
                                          occurrence_table[group_number].keys()))

    return result


def _des_gen_key_pc_1_inv(bs: BitString) -> BitString:
    result = bit_string.permutation_by_table_with_completion(bs, _des_gen_key_pc_1_inv_table)

    _des_gen_key_pc_2_inv_block_length = 8

    parity_bit_list = []

    result_block_list = [result[i:i + _des_gen_key_pc_2_inv_block_length - 1]
                         for i in range(0, des_orig_key_length, _des_gen_key_pc_2_inv_block_length)]

    for block in result_block_list:
        one_count = len(list(filter(lambda x: ord(x) == bit_string.ord_1, block)))

        parity_bit_list.append(BitString('1') if one_count % 2 == 0 else BitString('0'))

    result = BitString(''.join(map(operator.add, result_block_list, parity_bit_list)))

    return result


def _des_gen_key_pc_2_inv(bs: BitString) -> BitString:
    return bit_string.permutation_by_table(bs, _des_gen_key_pc_2_inv_table)


def _des_3round_iter_possible_keys(possible_key_chunks: List[Set[BitString]]):
    mid = _des_actual_key_length // 2
    total_left_rshift_rounds = sum(_des_gen_key_shift_count_table[0:_des_3round_round_count])

    for known_bits in itertools.product(*possible_key_chunks):
        for unknown_bits in itertools.product(*itertools.repeat(bit_string.all_bits, _des_s_group_count)):
            # 从 DES 轮密钥结构推出
            curr_k_3 = BitString(''.join(known_bits) + ''.join(unknown_bits))

            curr_k_0 = _des_gen_key_pc_2_inv(curr_k_3)
            # XXX: why curr_k_0[:mid] and curr_k_0_l + curr_k_0_r still return a str?
            curr_k_0_l = bit_string.right_rshift(BitString(curr_k_0[:mid]), total_left_rshift_rounds)
            curr_k_0_r = bit_string.right_rshift(BitString(curr_k_0[mid:]), total_left_rshift_rounds)
            curr_k_0 = operator.add(curr_k_0_l, curr_k_0_r)

            curr_k = _des_gen_key_pc_1_inv(curr_k_0)

            yield curr_k

    return


def des_3round_cryptanalysis_differential(p: List[bytes], c: List[bytes]) -> List[bytes]:
    if len(p) != len(c):
        raise ValueError(__name__ + ": count of ciphertext and plaintext does not match")

    p_length = len(p)

    if p_length == 0:
        raise ValueError(__name__ + ": empty text lists")

    if p_length % 2 != 0:
        raise ValueError(__name__ + ": c_list of odd length")

    p_list = list(map(bit_string.bytes_to_bit_string, p))
    c_list = list(map(bit_string.bytes_to_bit_string, c))

    possible_key_chunks = _des_3round_cryptanalysis_differential_gen_possible_key_chunks(p_list, c_list)
    result = []

    for possible_key in _des_3round_iter_possible_keys(possible_key_chunks):
        possible_key_bytes = bit_string.bit_string_to_bytes(possible_key)

        if list(map(lambda x: des_3round_encrypt(x, possible_key_bytes), p)) == c:
            result.append(possible_key_bytes)

    return result


def encrypt_file(p_path: str, c_path: str, k: bytes) -> None:
    fi = open(p_path, 'rb')
    fo = open(c_path, 'wb')

    while True:
        curr_bytes = fi.read(8)

        if len(curr_bytes) == 0:
            break

        if len(curr_bytes) < 8:
            curr_bytes = curr_bytes + bytes(8 - len(curr_bytes))

        fo.write(encrypt(curr_bytes, k))

    fi.close()
    fo.close()


def decrypt_file(p_path: str, c_path: str, k: bytes) -> None:
    fi = open(c_path, 'rb')
    fo = open(p_path, 'wb')

    while True:
        curr_bytes = fi.read(8)

        if len(curr_bytes) == 0:
            break

        if len(curr_bytes) < 8:
            curr_bytes = curr_bytes + bytes(8 - len(curr_bytes))

        fo.write(decrypt(curr_bytes, k))

    fi.close()
    fo.close()
