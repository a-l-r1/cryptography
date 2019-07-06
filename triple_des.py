import des


_e = des.encrypt
_d = des.decrypt


def _triple_des_check(b: bytes, k1: bytes, k2: bytes) -> None:
    if len(b) != des.des_block_length // 8:
        raise ValueError("des_encrypt: p not of %d bits" % des.des_block_length)

    for i in (k1, k2):
        if len(i) != des.des_orig_key_length // 8:
            raise ValueError("des_encrypt: %s not of %d bits" % (i.__name__, des.des_orig_key_length))


def encrypt(p: bytes, k1: bytes, k2: bytes) -> bytes:
    _triple_des_check(p, k1, k2)

    return _e(_d(_e(p, k1), k2), k1)


def decrypt(c: bytes, k1: bytes, k2: bytes) -> bytes:
    _triple_des_check(c, k1, k2)

    return _d(_e(_d(c, k1), k2), k1)
