import secrets
from typing import Tuple

import dss_common
import gcd
import modular_exp


p = int(
    "17801190547854226652823756245015999014523215636912067427327445031"
    "444286578873702077061269525212346307956715678477846644997065077092072"
    "785705000966838814403412974522117181850604723115003930107995935806739"
    "534871706631980226201971496652413506094591370759495651467285569060679"
    "4135837542707371727429551343320695239"
)
q = int(
    "864205495604807476120572616017955259175325408501"
)
g = int(
    "17406820753240209518581198012352343653860449079456135097849583104"
    "059995348845582314785159740894095072530779709491575949236830057425243"
    "876103708447346718014887611810308304375498519098347260155049469132948"
    "808339549231385000036164648264460849230407872181895999905649609776936"
    "8017749273708962006689187956744210730"
)


def gen_key() -> Tuple[int, int]:
    # [1, q - 1] -> [0, q - 2] -> [0, q - 1)
    x = secrets.randbelow(q - 1)
    x += 1

    y = modular_exp.modular_exp(g, x, p)

    return x, y


def sign(m: bytes, sk: int) -> Tuple[int, int]:
    while True:
        # [1, q - 1] -> [0, q - 2] -> [0, q - 1)
        k = secrets.randbelow(q - 1)
        k += 1

        x = sk

        r = (modular_exp.modular_exp(g, k, p)) % q
        s = (gcd.get_modular_inverse(k, q) * (dss_common.dss_hash(m) + x * r)) % q

        if r != 0 and s != 0:
            return r, s


def verify(m: bytes, pk: int, sig: Tuple[int, int]) -> bool:
    r, s = sig
    y = pk

    if not (0 < r < q and 0 < s < q):
        print('111')
        return False

    w = None
    try:
        w = gcd.get_modular_inverse(s, q)
    except ValueError:
        return False

    u_1 = (dss_common.dss_hash(m) * w) % q
    u_2 = (r * w) % q

    v = ((modular_exp.modular_exp(g, u_1, p) * modular_exp.modular_exp(y, u_2, p)) % p) % q

    return v == r
