import itertools
from typing import Dict, Iterator, List


_ord_space = ord(' ')
_ord_backspace = 0x08


def _permute(b: bytes, pigeonhole_list: List, id_: int) -> bytes:
    pigeonhole_count = len(pigeonhole_list)
    pigeonhole_insert_count = [id_ // pigeonhole_count] * pigeonhole_count
    pigeonhole_insert_count[id_ % pigeonhole_count] += 1

    offset = 0
    for i in range(len(pigeonhole_list)):
        b = _insert_magic_before_index(b, pigeonhole_list[i] + offset, pigeonhole_insert_count[i])
        offset += pigeonhole_insert_count[i] * 2

    return b


def _insert_magic_before_index(b: bytes, index: int, count: int) -> bytes:
    b1 = b[:index]
    b2 = bytes((_ord_space, _ord_backspace)) * count
    b3 = b[index:]

    return b1 + b2 + b3


def _get_pigeonhole_list(b: bytes) -> List[int]:
    result = []

    for index in range(len(b)):
        if b[index] == _ord_space:
            result.append(index)

    return result


def iter_permutation(m: bytes) -> Iterator[bytes]:
    pigeonhole_list = _get_pigeonhole_list(m)
    pigeonhole_count = len(pigeonhole_list)
    if pigeonhole_count == 0:
        raise ValueError("iter_permutation(): no space in message")

    id_ = 0
    while True:
        yield _permute(m, pigeonhole_list, id_)
        id_ += 1


def get_permutation_list(m: bytes, count: int) -> List[bytes]:
    result = []

    i = iter_permutation(m)

    curr_count = 0
    while curr_count <= count:
        result.append(next(i))
        curr_count += 1

    return result
