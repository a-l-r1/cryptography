import pickle
import secrets

from typing import List, Tuple

import cipher_common
import gcd
import lll

from bit_string import BitString


_key_w_0_upper_bound = 100
_q_delta_upper_bound = 10000


def gen_key(length: int) -> Tuple[Tuple[List[int], int, int], List[int]]:
    if length <= 0:
        raise ValueError("gen_key(): length <= 0")
    w_1 = secrets.randbelow(_key_w_0_upper_bound)

    w = [0 for _ in range(length)]
    w[0] = w_1

    for i in range(1, length):
        w[i] = w[i - 1] * 2 + 1

    q = sum(w) + secrets.randbelow(_q_delta_upper_bound) + 1

    r = 0
    while gcd.gcd(r, q) != 1:
        r = secrets.randbelow(q)

    pk = list(map(lambda w_i: (r * w_i) % q, w))

    return (w, q, r), pk


def encrypt(m: BitString, pk: List[int]) -> int:
    return sum(map(lambda alpha_i, beta_i: int(alpha_i) * beta_i, m, pk))


def write_secret_key(filename: str, sk: Tuple[List[int], int, int]) -> None:
    pickle.dump(sk, filename)


def write_public_key(filename: str, pk: List[int]) -> None:
    pickle.dump(pk, filename)


def read_secret_key(filename: str) -> Tuple[List[int], int, int]:
    return pickle.load(filename)


def read_public_key(filename: str) -> List[int]:
    return pickle.load(filename)


# TODO: file encrytion and decryption


def decrypt(c: int, sk: Tuple[List[int], int, int]) -> BitString:
    result = ''
    w = sk[0]
    q = sk[1]
    r = sk[2]

    if gcd.gcd(q, r) != 1:
        raise ValueError("decrypt(): q and r not coprime")

    c_real = (c * gcd.get_modular_inverse(r, q)) % q

    for w_i in reversed(w):
        if c_real >= w_i:
            c_real -= w_i
            result += '1'
        else:
            result += '0'

        if c_real < 0:
            raise ValueError("decrypt(): decrypt error")

    if c_real != 0:
        raise ValueError("decrypt(): decrypt error")

    return BitString(result)


def cryptanalysis_lll(c: int, pk: List[int]) -> BitString:
    delta = 0.75

    if len(pk) <= 1:
        raise ValueError("cryptanalysis_lll(): pk too short")

    n = len(pk) + 1

    m = [[0 for _ in range(n)] for _ in range(n)]

    # fill in identity matrix
    for i in range(n - 1):
        m[i][i] = 1

    # fill in public key
    for i in range(n - 1):
        m[i][n - 1] = pk[i]

    m[n - 1][n - 1] = -c

    m_lll = lll.lll(m, delta)
    print(m_lll)

    valid_row = None

    for row in m_lll:
        is_valid = True

        for elem in row[:-1]:
            if elem != 0 and elem != 1:
                is_valid = False

        if row[-1] != 0:
            is_valid = False

        if is_valid:
            valid_row = row

    if valid_row is None:
        raise ValueError("cryptanalysis_lll(): cryptanalysis failed")

    return BitString(''.join(map(str, valid_row[:-1])))
