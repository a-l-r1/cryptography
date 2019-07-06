import itertools
from typing import Callable, Iterable

_hmac_ipad_byte = 0x36
_hmac_opad_byte = 0x5c


def merkle_damgard_wide_pipe(iv: bytes, blocks: Iterable[bytes], f: Callable[[bytes, bytes], bytes],
                             block_length: int, output_length: int) -> bytes:
    if len(iv) != output_length:
        raise ValueError("merkle_damgard_wide_pipe: broken iv: length != output length")

    result = iv

    for block in blocks:
        if len(block) != block_length:
            raise ValueError("merkle_damgard_wide_pipe: broken block: length != block length")

        result = f(block, result)

        if len(result) != output_length:
            raise ValueError("merkle_damgard_wide_pipe: broken output of f: length != output length")

    return result


def hmac(m: bytes, k: bytes, f_digest: Callable[[bytes], bytes],
         block_length: int) -> bytes:
    if len(k) > block_length:
        k = f_digest(k)

    k_right_padding_length = block_length - len(k)
    k_plus = k + bytes(k_right_padding_length)

    k_s1 = bytes(x ^ y for x, y in zip(k_plus, itertools.repeat(_hmac_ipad_byte)))
    hash_s1 = f_digest(k_s1 + m)

    k_s2 = bytes(x ^ y for x, y in zip(k_plus, itertools.repeat(_hmac_opad_byte)))
    hash_s2 = f_digest(k_s2 + hash_s1)

    return hash_s2
