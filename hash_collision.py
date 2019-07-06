import secrets
import hashlib

from typing import Callable, List, Tuple


_bytes_length_upper_bound = 256
_hash_truncate_length = 2


def gen_rand_bytes() -> bytes:
    # avoid bytes with length 0
    return bytes(secrets.randbelow(1 << 8) for _ in range(secrets.randbelow(_bytes_length_upper_bound - 1) + 1))


def hash_(m: bytes) -> bytes:
    return hashlib.sha1(m).digest()[:_hash_truncate_length]


def find_collision_pair(rand_bytes_generator_func: Callable[[], bytes],
                        hash_func: Callable[[bytes], bytes]) -> Tuple[bytes, bytes]:
    b1 = rand_bytes_generator_func()
    b2 = rand_bytes_generator_func()

    tries = 1

    while hash_func(b1) != hash_func(b2) or b1 == b2:
        b1, b2 = rand_bytes_generator_func(), rand_bytes_generator_func()

        tries += 1
        if tries % 1024 == 0:
            print(tries)

    print('tries used: %d' % tries)
    return b1, b2
