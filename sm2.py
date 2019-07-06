import secrets
from typing import Tuple

import ec
import sm3
from sm2_common import *

_hash_output_length = 256


def _int_div_round_up(dividend: int, divisor: int) -> int:
    if dividend % divisor == 0:
        return dividend // divisor
    else:
        return dividend // divisor + 1


_hash = sm3.digest


def _kdf(z: bytes, k_len: int) -> bytes:
    if k_len % 8 != 0:
        raise ValueError("_kgf(): unsupported key length")

    ct = 1
    v = _hash_output_length

    # make indices match the spec
    h_a = [b'']

    for i in range(1, _int_div_round_up(k_len, v) + 1):
        h_a.append(_hash(z + int.to_bytes(ct, 32 // 8, 'big')))
        ct += 1

    if k_len % v != 0:
        h_a[_int_div_round_up(k_len, v)] = \
            h_a[_int_div_round_up(k_len, v)][:(k_len - (v * (k_len // v))) // 8]

    return bytes.join(bytes(), h_a)


def _fp_element_to_bytes(n_: fp) -> bytes:
    t = n_.p.bit_length()
    length = _int_div_round_up(t, 8)

    return int.to_bytes(n_.data, length, 'big')


def _ecpoint_to_bytes(p_: ECPoint) -> bytes:
    if p_.is_infinite:
        raise ValueError("_ecpoint_to_bytes(): p is infinite")

    x_1 = _fp_element_to_bytes(p_.x)
    y_1 = _fp_element_to_bytes(p_.y)

    pc = bytes((0x04,))

    return pc + x_1 + y_1


def gen_key() -> Tuple[fp, ECPoint]:
    # [1, n - 2] -> [0, n - 3] -> [0, n - 2)
    d = secrets.randbelow(n - 2)
    p_ = d * g
    d = fp(d)

    return d, p_


def encrypt(m: bytes, pk: ECPoint) -> bytes:
    completed = False
    x_2, y_2 = None, None
    c_1, c_2, c_3 = None, None, None
    t = None

    while not completed:
        # [1, n - 1] -> [0, n - 2)
        k = secrets.randbelow(n - 2)

        c_1 = k * g
        c_1 = _ecpoint_to_bytes(c_1)

        p_b = pk
        h = 1

        s = h * p_b
        if s.is_infinite:
            raise ValueError("encrypt(): s is infinite point")
        k_p_b = k * s

        x_2 = k_p_b.x
        y_2 = k_p_b.y
        x_2 = _fp_element_to_bytes(x_2)
        y_2 = _fp_element_to_bytes(y_2)

        k_len = len(m) * 8

        t = _kdf(x_2 + y_2, k_len)

        for byte in t:
            if byte != 0:
                completed = True

    c_2 = bytes(x ^ y for x, y in zip(m, t))
    c_3 = _hash(x_2 + m + y_2)

    return c_1 + c_2 + c_3


def decrypt(c: bytes, sk: fp) -> bytes:
    # TODO: support other formats
    if c[0] != 0x04:
        raise ValueError("decrypt(): unsupported point format")

    # determine byte length of p from sk
    length = _int_div_round_up(sk.p.bit_length(), 8)

    try:
        c_1 = c[:2 * length + 1]
        c_1 = ECPoint(ec, fp(int.from_bytes(c_1[1:length + 1], 'big')),
                      fp(int.from_bytes(c_1[length + 1:2 * length + 1], 'big')))

        if c_1.y * c_1.y != c_1.x * c_1.x * c_1.x + c_1.ec.a * c_1.x + c_1.ec.b:
            raise ValueError

        if c_1.is_infinite:
            raise ValueError

        c_2 = c[2 * length + 1: - _hash_output_length // 8]
        c_3 = c[- _hash_output_length // 8:]
    except IndexError:
        raise ValueError("decrypt(): bad ciphertext format")
    except ValueError:
        raise ValueError("decrypt(): invalid c_1: not on the curve or is infinite")

    sk_c_1 = sk.data * c_1
    x_2 = sk_c_1.x
    y_2 = sk_c_1.y
    x_2 = _fp_element_to_bytes(x_2)
    y_2 = _fp_element_to_bytes(y_2)

    k_len = len(c_2) * 8
    t = _kdf(x_2 + y_2, k_len)

    for byte in t:
        if byte != 0:
            break
    else:
        raise ValueError("decrypt(): all bytes of t are zero")

    m_ = bytes(x ^ y for x, y in zip(c_2, t))

    u = _hash(x_2 + m_ + y_2)

    if u != c_3:
        raise ValueError("decrypt(): invalid ciphertext")

    return m_


def encrypt_file(pt_filename: str, ct_filename: str, pk: ECPoint) -> None:
    with open(pt_filename, 'rb') as pt_f, open(ct_filename, 'wb') as ct_f:
        m = pt_f.read()
        c = encrypt(m, pk)
        ct_f.write(c)


def decrypt_file(pt_filename: str, ct_filename: str, sk: fp) -> None:
    with open(pt_filename, 'wb') as pt_f, open(ct_filename, 'rb') as ct_f:
        c = ct_f.read()
        m = decrypt(c, sk)
        pt_f.write(m)
