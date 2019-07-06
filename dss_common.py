import hashlib

p = 265371653


def dss_hash(m: bytes) -> int:
    # SHA-256 is known for its collision resistance
    return int.from_bytes(hashlib.sha256(m).digest(), 'big')


def dss_hash_modular(m: bytes) -> int:
    return dss_hash(m) % p
