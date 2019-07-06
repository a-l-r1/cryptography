from typing import Tuple

import gcd
import letter


def _check_key(k: Tuple[int]) -> None:
    if len(k) != 2:
        raise ValueError("_check_key: key length must be 2")

    for i in k:
        if i < 0 or i > letter.LETTER_COUNT - 1:
            raise ValueError("_check_key: %s: key not in [0, 25]" % \
                             str(k))

    if gcd.gcd(k[0], 26) != 1:
        raise ValueError("_check_key: %s: a not coprime with 26" % \
                         str(k))


def _letter_mul_shift(m: str, k: Tuple[int], base: int) -> str:
    return chr((k[0] * (ord(m) - base) + k[1]) % letter.LETTER_COUNT + \
               base)


def _letter_shift_mul(m: str, k: Tuple[int], base: int) -> str:
    return chr((((ord(m) - base) + k[1]) * k[0]) % \
               letter.LETTER_COUNT + base)


def encrypt(s: str, k: Tuple[int]) -> str:
    _check_key(k)
    s = s.upper()

    return ''.join(map(lambda x: _letter_mul_shift(x, k,
                                                   letter.ORD_BASE_CAPITAL_A) if x.isupper() else x, s))


def encrypt_nocheck(s: str, k: Tuple[int]) -> str:
    s = s.upper()

    return ''.join(map(lambda x: _letter_mul_shift(x, k,
                                                   letter.ORD_BASE_CAPITAL_A), s))


def decrypt(s: str, k: Tuple[int]) -> str:
    _check_key(k)
    s = s.upper()

    k_d = (gcd.get_modular_inverse(k[0], letter.LETTER_COUNT), -k[1])

    return ''.join(map(lambda x: _letter_shift_mul(x, k_d,
                                                   letter.ORD_BASE_CAPITAL_A) if x.isupper() else x, s))


def decrypt_nocheck(s: str, k: Tuple[int]) -> str:
    s = s.upper()

    k_d = (gcd.get_modular_inverse(k[0], letter.LETTER_COUNT), -k[1])

    return ''.join(map(lambda x: _letter_shift_mul(x, k_d, \
                                                   letter.ORD_BASE_CAPITAL_A), s))
