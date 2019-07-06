import secrets
from typing import Tuple

import gcd
import modular_exp
from dss_common import dss_hash

# g = 154868156
# g_inv = gcd.get_modular_inverse(g, p)
# q = 104149

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
g_inv = gcd.get_modular_inverse(g, p)


def gen_key() -> Tuple[int, int]:
    # (0, q) -> [0, q - 1)
    s = secrets.randbelow(q - 1) + 1

    v = modular_exp.modular_exp(g_inv, s, p)

    return s, v


def sign(m: bytes, sk: int) -> Tuple[int, int]:
    s = sk

    # (0, q) -> [0, q - 1)
    r = secrets.randbelow(q - 1)

    x = modular_exp.modular_exp(g, r, p)

    e = dss_hash(bytes(str(x), encoding='us-ascii') + m) % p

    y = (r + s * e) % q

    return e, y


def verify(m: bytes, pk: int, sig: Tuple[int, int]) -> bool:
    e, y = sig
    v = pk

    x = (modular_exp.modular_exp(g, y, p) * modular_exp.modular_exp(v, e, p)) % p

    return dss_hash(bytes(str(x), encoding='us-ascii') + m) % p == e
