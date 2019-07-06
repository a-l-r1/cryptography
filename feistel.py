from typing import Callable, List

import bit_string
from bit_string import BitString


def feistel_round(s: BitString, k: BitString, f: Callable[[BitString, BitString], BitString]) -> BitString:
    length = len(s)

    if length % 2 != 0:
        raise ValueError("feistel_round: s not of even length")

    l = BitString(s[0:length // 2])
    r = BitString(s[length // 2:])

    l_new = r
    r_new = bit_string.xor(l, f(r, k))

    result = BitString(l_new + r_new)

    return result


def feistel_repetitive(s: BitString, key_list: List[BitString], f: Callable[[BitString, BitString], BitString],
                       rounds: int) -> BitString:
    if len(key_list) != rounds:
        raise ValueError("feistel_repetitive: key list length != rounds")

    result = s

    for i in range(rounds):
        result = feistel_round(result, key_list[i], f)

    return result
