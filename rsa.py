import gcd
import primality_test
import modular_exp

import secrets
from typing import Tuple

_endian = 'little'
_primality_test_iterations = 20
_e = 65537
_e_length = 4


def _check_size(size: int) -> None:
    if not size > 0:
        raise ValueError(__name__ + ": size is non-positive")

    if size % 2 != 0:
        raise ValueError(__name__ + ": size must be even")


def _encrypt(m: int, e: int, n: int) -> int:
    return modular_exp.modular_exp(m, e, n)


def _decrypt(c: int, d: int, n: int) -> int:
    return modular_exp.modular_exp(c, d, n)


def _gen_prime(size: int) -> int:
    while True:
        result = secrets.randbits(size)

        if primality_test.primality_test(result, _primality_test_iterations):
            break

    return result


def gen_key(size: int) -> Tuple[Tuple, Tuple[int, int]]:
    # XXX: correct?
    _check_size(size)

    p = _gen_prime(size // 2)
    q = _gen_prime(size // 2)

    phi_n = (p - 1) * (q - 1)
    d = gcd.get_modular_inverse(_e, phi_n)

    sk = tuple(map(lambda x: x.to_bytes(size // 2, _endian, signed=False), (p, q, d)))

    n = p * q
    e = _e

    pk = (n, e)

    return sk, pk


def encrypt(p: bytes, pk: Tuple[bytes, bytes]):
    pass


def decrypt(c: bytes, ck: Tuple[bytes, bytes]):
    pass
