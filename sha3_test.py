import hashlib
import hmac as hmac_
import secrets

from sha3 import *


_iterations = 200
_length_upper_bound = 1000


def main() -> None:
    for bit_length in [224, 256, 384, 512]:
        print('testing bit_length %d' % bit_length)

        for i in range(_iterations):
            curr_length = secrets.randbelow(_length_upper_bound)
            curr_key_length = secrets.randbelow(_length_upper_bound)
            curr_bytes = bytes((secrets.randbelow(1 << 8) for _ in range(curr_length)))
            curr_key_bytes = bytes((secrets.randbelow(1 << 8) for _ in range(curr_key_length)))

            # dynamic name lookup
            own_hash = globals()['digest_' + str(bit_length)](curr_bytes).hex()
            ref_hash = getattr(hashlib, 'sha3_' + str(bit_length))(curr_bytes).hexdigest()

            own_hmac = globals()['hmac_' + str(bit_length)](curr_bytes, curr_key_bytes).hex()
            ref_hmac = hmac_.new(curr_key_bytes, curr_bytes,
                                 getattr(hashlib, 'sha3_' + str(bit_length))).digest().hex()

            if own_hash != ref_hash:
                print(i)
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
