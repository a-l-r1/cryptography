import secrets
from typing import Tuple

import gcd
import modular_exp
from dss_common import *

g = 2


def gen_key() -> Tuple[int, Tuple[int, int, int]]:
    # (1, p - 1) -> [0, p - 2)
    x = secrets.randbelow(p - 2) + 1

    y = modular_exp.modular_exp(g, x, p)

    return x, (y, p, g)


def sign(m: bytes, sk: int) -> Tuple[int, int]:
    m = dss_hash(m)
    x = sk

    k = 0
    while not (k > 1 and gcd.is_coprime(k, p - 1)):
        k = secrets.randbelow(p - 1)

    s_1 = modular_exp.modular_exp(g, k, p)
    s_2 = (gcd.get_modular_inverse(k, p - 1) * (m - x * s_1)) % (p - 1)

    return s_1, s_2


def verify(m: bytes, pk: Tuple[int, int, int], sig: Tuple[int, int]) -> bool:
    y, p_, g_ = pk
    s_1, s_2 = sig
    m = dss_hash(m)

    v_1 = modular_exp.modular_exp(g_, m, p_)
    v_2 = (modular_exp.modular_exp(y, s_1, p_) * modular_exp.modular_exp(s_1, s_2, p_)) % p_

    return v_1 == v_2
