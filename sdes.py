from typing import List, Dict, Tuple, Set
import operator

import feistel
import bit_string
from bit_string import BitString

_sdes_key_length = 10
_sdes_gen_key_rounds = 2

_sdes_gen_key_p10_table = [
    3, 5, 2, 7, 4, 10, 1, 9, 8, 6
]

_sdes_gen_key_lshift_count_table = [
    1, 2
]

_sdes_gen_key_p8_table = [
    6, 3, 7, 4, 8, 5, 10, 9
]

_sdes_rounds = 2
_sdes_block_length = 8

_sdes_ip_table = [
    2, 6, 3, 1, 4, 8, 5, 7
]

_sdes_e_table = [
    4, 1, 2, 3, 2, 3, 4, 1
]

_sdes_s_input_length = 4

_sdes_s_row_determination_table = {
    BitString('00'): 0,
    BitString('01'): 1,
    BitString('10'): 2,
    BitString('11'): 3
}

_sdes_s_table = [
    [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
    ],
    [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]
    ]
]

_sdes_p4_table = [
    2, 4, 3, 1
]

_sdes_ip_inv_table = [
    4, 1, 3, 5, 7, 2, 8, 6
]


def _sdes_gen_key(k: BitString) -> List[BitString]:
    actual_key = bit_string.permutation_by_table(k, _sdes_gen_key_p10_table)

    result = []

    key_l = actual_key[:_sdes_key_length // 2]
    key_r = actual_key[_sdes_key_length // 2:]

    for i in range(_sdes_gen_key_rounds):
        key_l = bit_string.left_rshift(key_l, _sdes_gen_key_lshift_count_table[i])
        key_r = bit_string.left_rshift(key_r, _sdes_gen_key_lshift_count_table[i])

        result.append(bit_string.permutation_by_table(operator.add(key_l, key_r), _sdes_gen_key_p8_table))

    return result


def _sdes_ip(bs: BitString) -> BitString:
    return bit_string.permutation_by_table(bs, _sdes_ip_table)


def _sdes_e(bs: BitString) -> BitString:
    return bit_string.permutation_by_table(bs, _sdes_e_table)


def _sdes_s_single_box(bs: BitString, i: int) -> BitString:
    bs_l = BitString(bs[0] + bs[3])
    bs_r = BitString(bs[1] + bs[2])

    result = _sdes_s_table[i][_sdes_s_row_determination_table[bs_l]][_sdes_s_row_determination_table[bs_r]]

    return bit_string.small_int_to_bit_string(result, _sdes_s_input_length // 2)


def _sdes_s(bs: BitString) -> BitString:
    bs_l = BitString(bs[:_sdes_block_length // 2])
    bs_r = BitString(bs[_sdes_block_length // 2:])

    result_l = _sdes_s_single_box(bs_l, 0)
    result_r = _sdes_s_single_box(bs_r, 1)

    return operator.add(result_l, result_r)


def _sdes_p4(bs: BitString) -> BitString:
    return bit_string.permutation_by_table(bs, _sdes_p4_table)


def _sdes_f(bs: BitString, k: BitString) -> BitString:
    result = _sdes_e(bs)
    result = bit_string.xor(result, k)
    result = _sdes_s(result)
    result = _sdes_p4(result)

    return result


def _sdes_ip_inv(bs: BitString) -> BitString:
    return bit_string.permutation_by_table(bs, _sdes_ip_inv_table)


def _sdes(bs: BitString, key_list: List[BitString]) -> BitString:
    result = _sdes_ip(bs)

    result_l = BitString(result[:_sdes_block_length // 2])
    result_r = BitString(result[_sdes_block_length // 2:])

    result_l = bit_string.xor(result_l, _sdes_f(result_r, key_list[0]))
    result_l, result_r = result_r, result_l
    result_l = bit_string.xor(result_l, _sdes_f(result_r, key_list[1]))
    result = operator.add(result_l, result_r)

    result = _sdes_ip_inv(result)
    return result


def _sdes_check_text(bs: BitString) -> None:
    if len(bs) != _sdes_block_length:
        raise ValueError(__name__ + ": text length != %d" % _sdes_block_length)


def _sdes_check_key(k: BitString) -> None:
    if len(k) != _sdes_key_length:
        raise ValueError(__name__ + ": key length != %d" % _sdes_key_length)


def encrypt(p: BitString, k: BitString) -> BitString:
    _sdes_check_text(p)
    _sdes_check_key(k)

    key_list = _sdes_gen_key(k)

    return _sdes(p, key_list)


def decrypt(c: BitString, k: BitString) -> BitString:
    _sdes_check_text(c)
    _sdes_check_key(k)

    key_list = _sdes_gen_key(k)
    key_list.reverse()

    return _sdes(c, key_list)


def double_sdes_encrypt(p: BitString, k1: BitString, k2: BitString) -> BitString:
    _sdes_check_text(p)
    _sdes_check_key(k1)
    _sdes_check_key(k2)

    return encrypt(encrypt(p, k1), k2)


def double_sdes_decrypt(c: BitString, k1: BitString, k2: BitString) -> BitString:
    _sdes_check_text(c)
    _sdes_check_key(k1)
    _sdes_check_key(k2)

    return decrypt(decrypt(c, k2), k1)


def _double_sdes_cryptanalysis_mitm_gen_possible_key_pairs(p: BitString, c: BitString) -> \
        Set[Tuple[BitString, BitString]]:
    s1_dict: Dict[BitString, List[BitString]] = {}

    for key_int in range(1 << _sdes_key_length):
        key = bit_string.small_int_to_bit_string(key_int, _sdes_key_length)
        curr_encrypt_result = encrypt(p, key)

        if curr_encrypt_result not in s1_dict:
            s1_dict[curr_encrypt_result] = [key]
        else:
            s1_dict[curr_encrypt_result].append(key)

    result = set()

    for key_int in range(1 << _sdes_key_length):
        key = bit_string.small_int_to_bit_string(key_int, _sdes_key_length)
        curr_decrypt_result = decrypt(c, key)

        if curr_decrypt_result in s1_dict:
            for key_pair in map(lambda x: (x, key), s1_dict[curr_decrypt_result]):
                result.add(key_pair)

    return result


def double_sdes_cryptanalysis_mitm(p_list: List[BitString], c_list: List[BitString]) -> Set[BitString]:
    _double_sdes_cryptanalysis_mitm_pair_count = 2

    if len(p_list) != len(c_list):
        raise ValueError(__name__ + ": plaintext and ciphertext not of the same amount")

    if len(p_list) < _double_sdes_cryptanalysis_mitm_pair_count:
        raise ValueError(__name__ + ": parameters must be at least %d pairs" %
                         _double_sdes_cryptanalysis_mitm_pair_count)

    pkp_set = _double_sdes_cryptanalysis_mitm_gen_possible_key_pairs(p_list[0], c_list[0])

    for i in range(1, _double_sdes_cryptanalysis_mitm_pair_count):
        new_pkp_set = set()

        for key_pair in pkp_set:
            if double_sdes_encrypt(p_list[i], key_pair[0], key_pair[1]) == c_list[i]:
                new_pkp_set.add(key_pair)

        pkp_set = new_pkp_set

        if len(pkp_set) == 0:
            raise ValueError(__name__ + ": no possible key pairs")

    return pkp_set
