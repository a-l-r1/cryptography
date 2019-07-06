import secrets
from gmssl import sm3, func

from sm3 import *


_iterations = 10000
_length_upper_bound = 1000


def hash_(m: bytes) -> bytes:
    return sm3.sm3_hash(func.bytes_to_list(m))


def main() -> None:
    for i in range(_iterations):
        curr_length = secrets.randbelow(_length_upper_bound)
        curr_key_length = secrets.randbelow(_length_upper_bound)
        curr_bytes = bytes((secrets.randbelow(1 << 8) for _ in range(curr_length)))
        curr_key_bytes = bytes((secrets.randbelow(1 << 8) for _ in range(curr_key_length)))

        own_hash = digest(curr_bytes).hex()
        ref_hash = hash_(curr_bytes)

        if own_hash != ref_hash:
            print("hash mismatch: ")
            print(curr_bytes.hex())
            break
    else:
        print("test passed")


if __name__ == '__main__':
    main()

