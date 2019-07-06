import secrets
from typing import Tuple

import ec
import gcd
import sm3
from sm2 import *
from sm2_common import *


def _int_div_round_up(dividend: int, divisor: int) -> int:
    if dividend % divisor == 0:
        return dividend // divisor
    else:
        return dividend // divisor + 1


def _fp_element_to_bytes(n_: fp) -> bytes:
    t = n_.p.bit_length()
    length = _int_div_round_up(t, 8)

    return int.to_bytes(n_.data, length, 'big')


_hash = sm3.digest


def get_user_hash(id_: bytes, pk: ECPoint) -> bytes:
    entlen = len(id_) * 8
    entl = entlen.to_bytes(2, 'big')

    a_bytes = _fp_element_to_bytes(ec.a)
    b_bytes = _fp_element_to_bytes(ec.b)
    x_g_bytes = _fp_element_to_bytes(g.x)
    y_g_bytes = _fp_element_to_bytes(g.y)
    x_a_bytes = _fp_element_to_bytes(pk.x)
    y_a_bytes = _fp_element_to_bytes(pk.y)

    return _hash(entl + id_ + a_bytes + b_bytes + x_g_bytes + y_g_bytes + x_a_bytes + y_a_bytes)


def gen_key() -> Tuple[fp, ECPoint]:
    # [1, n - 2] -> [0, n - 3] -> [0, n - 2)
    d = secrets.randbelow(n - 2)
    p_ = d * g
    d = fp(d)

    return d, p_


def sign(m: bytes, sk: fp, user_hash: bytes) -> bytes:
    m_bar = user_hash + m
    e = _hash(m_bar)
    e = int.from_bytes(e, 'big')

    r, s = None, None

    while True:
        # [1, n - 1] -> [0, n - 2] -> [0, n - 1)
        k = secrets.randbelow(n - 1)
        k += 1

        x = k * g

        x_1 = x.x
        x_1 = int(x_1)

        r = (e + x_1) % n

        if r == 0 and r + k == n:
            continue

        d_a = int(sk)
        s = (gcd.get_modular_inverse(1 + d_a, n) * (k - r * d_a)) % n

        if s == 0:
            continue
        else:
            break

    length = _int_div_round_up(n.bit_length(), 8)

    r_bytes = r.to_bytes(length, 'big')
    s_bytes = s.to_bytes(length, 'big')

    return r_bytes + s_bytes


def verify(m: bytes, pk: ECPoint, sig: bytes, user_hash: bytes) -> bool:
    try:
        length = _int_div_round_up(n.bit_length(), 8)

        r = sig[:length]
        s = sig[length:]

        if len(s) != length:
            raise ValueError

        r = int.from_bytes(r, 'big')
        s = int.from_bytes(s, 'big')

        if r < 1 or r > n - 1:
            return False

        if s < 1 or s > n - 1:
            return False
    except IndexError:
        return False
    except ValueError:
        return False

    m_bar_ = user_hash + m
    e_ = _hash(m_bar_)
    e_ = int.from_bytes(e_, 'big')

    t = (r + s) % n

    if t == 0:
        return False

    x = s * g + t * pk

    x_1_ = x.x
    x_1_ = int(x_1_)

    big_r = (e_ + x_1_) % n

    return big_r == r






