import itertools

import letter


def _check_key(k: str) -> None:
    if len(k) == 0:
        raise ValueError("_check_key: empty key")

    if any(map(lambda x: not x.isupper(), k.upper())):
        raise ValueError("_check_key: key contains non-uppercase")


def _letter_shift(m: str, k: str, base: str) -> str:
    return chr(((ord(m) - base) + (ord(k) - base)) % 26 + base)


def _letter_shift_back(m: str, k: str, base: str) -> str:
    return chr(((ord(m) - base) - (ord(k) - base)) % 26 + base)


def _skip_non_letter_iter(s: str, k: str) -> str:
    k_cycle = itertools.cycle(k)

    for i in s:
        if i.isupper():
            yield next(k_cycle)
        else:
            yield None

    return


def encrypt(s: str, k: str) -> str:
    _check_key(k)
    s = s.upper()
    k = k.upper()

    return ''.join(map( \
        lambda x, y: _letter_shift(x, y, letter.ORD_BASE_CAPITAL_A) \
            if x.isupper() else x, \
        s, _skip_non_letter_iter(s, k)))


def encrypt_nocheck(s: str, k: str) -> str:
    s = s.upper()

    return ''.join(map( \
        lambda x, y: _letter_shift(x, y, letter.ORD_BASE_CAPITAL_A), \
        s, _skip_non_letter_iter(s, k)))


def decrypt(s: str, k: str) -> str:
    _check_key(k)
    s = s.upper()
    k = k.upper()

    return ''.join(map( \
        lambda x, y: _letter_shift_back(x, y, \
                                        letter.ORD_BASE_CAPITAL_A) \
            if x.isupper() else x, \
        s, _skip_non_letter_iter(s, k)))


def decrypt_nocheck(s: str, k: str) -> str:
    s = s.upper()

    return ''.join(map( \
        lambda x, y: _letter_shift_back(x, y, \
                                        letter.ORD_BASE_CAPITAL_A), \
        s, _skip_non_letter_iter(s, k)))
