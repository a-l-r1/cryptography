import hashlib
import hmac as hmac_
import secrets

from sha1 import *


_iterations = 10000
_length_upper_bound = 1000


def main() -> None:
    for i in range(_iterations):
        curr_length = secrets.randbelow(_length_upper_bound)
        curr_key_length = secrets.randbelow(_length_upper_bound)
        curr_bytes = bytes((secrets.randbelow(1 << 8) for _ in range(curr_length)))
        curr_key_bytes = bytes((secrets.randbelow(1 << 8) for _ in range(curr_key_length)))

        own_hash = digest(curr_bytes).hex()
        ref_hash = hashlib.sha1(curr_bytes).hexdigest()

        own_hmac = hmac(curr_bytes, curr_key_bytes).hex()
        ref_hmac = hmac_.new(curr_key_bytes, curr_bytes, hashlib.sha1).digest().hex()

        if own_hash != ref_hash:
            print("hash mismatch: ")
            print(curr_bytes.hex())
            break

        if own_hmac != ref_hmac:
            print("HMAC mismatch: ")
            print(curr_bytes.hex())
            print(curr_key_bytes.hex())
            break
    else:
        print("test passed")


if __name__ == '__main__':
    main()
