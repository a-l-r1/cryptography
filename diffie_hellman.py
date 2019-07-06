import secrets
from typing import Tuple

from sm2_common import *


def gen_key() -> Tuple[fp, ECPoint]:
    x = secrets.randbelow(n)
    x = fp(x)

    return x, x * g


def retrieve_key(sk: fp, p_: ECPoint) -> ECPoint:
    return sk * p_
