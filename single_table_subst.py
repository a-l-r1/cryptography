import collections
import functools
import heapq
import itertools
import math
import operator
from typing import Dict, List

import letter

# 第一个参数是 D(p || q)，以便比较
key_d_entry = collections.namedtuple('key_entry', ['D', 'k_d'])


def _check_c_len(c: str) -> None:
    if len(letter.strip_whitespace(c)) == 0:
        raise ValueError("_check_c_len: empty ciphertext")


def _check_key(k: Dict[str, str]) -> None:
    if len(k) != letter.LETTER_COUNT:
        raise ValueError("_check_key: len(k) != letter count")

    if set(k.keys()) != letter.LETTER_SET:
        raise ValueError("_check_key: k.keys() must be the letter set")

    if set(k.values()) != letter.LETTER_SET:
        raise ValueError("_check_key: k.values() must be the letter set")


def _get_k_d(k: Dict[str, str]) -> Dict[str, str]:
    k_d = dict(map(lambda x: (k[x], x), k))
    return k_d


# 计算 D(实际分布 || 理想分布)
def _get_distance(freq: Dict[str, float], k: Dict[str, str]) -> float:
    return sum(map(lambda x: freq[k[x]] * math.log(freq[k[x]] / \
                                                   letter.LETTER_FREQ_DICT[x]) if k[x] in freq else 0.0,
                   letter.LETTER_SET))


def get_freq_num(c: str) -> collections.Counter:
    # 删掉空格
    c = letter.strip_whitespace(c)

    c = c.upper()
    c_counter = collections.Counter(c)

    if len(c_counter) > letter.LETTER_COUNT:
        raise ValueError("get_freq_num: > %d kinds of symbol" %
                         letter.LETTER_COUNT)

    for i in letter.LETTER_FREQ_LIST:
        if i not in c_counter:
            c_counter[i] = 0

    return c_counter


def get_freq(c: str) -> Dict[str, int]:
    _check_c_len(c)

    c_len = len(c)
    freq_num = get_freq_num(c)

    return dict(map(lambda x: (x, freq_num[x] / c_len), freq_num))


def encrypt(p: str, k: Dict[str, str]) -> str:
    _check_key(k)

    p = letter.strip_whitespace(p)
    p = p.upper()

    return p.translate(str.maketrans(k))


def encrypt_nocheck(p: str, k: Dict[str, str]) -> str:
    p = p.upper()

    return p.translate(str.maketrans(k))


def decrypt(c: str, k: Dict[str, str]) -> str:
    _check_key(k)
    c = c.upper()

    k_d = _get_k_d(k)

    return c.translate(str.maketrans(k_d))


def decrypt_nocheck(c: str, k: Dict[str, str]) -> str:
    k_d = dict(map(lambda x: (k[x], x), k))

    return c.translate(str.maketrans(k_d))


def get_base_decrypt_key(c: str) -> dict:
    freq = get_freq(c)

    sorted_letter_list = sorted(freq, key=freq.get, reverse=True)

    return dict(map(lambda x, y: (x, y), sorted_letter_list, letter.LETTER_FREQ_LIST))


_letter_freq_groups_list = \
    [['E', 'TAO', 'INSHR', 'DL', 'CU', 'MWFG', 'YP', 'BVK', 'JXQZ'],
     ['E', 'TAO', 'INSHR', 'DL', 'CU', 'MWF', 'GYP', 'BVK', 'JXQZ'],
     ['E', 'TAO', 'INSHR', 'DL', 'CU', 'MW', 'FGYP', 'BVK', 'JXQZ'],
     ['E', 'TAO', 'INSHR', 'DL', 'CU', 'MWFG', 'YPB', 'VK', 'JXQZ'],
     ['E', 'TAO', 'INSHR', 'DL', 'CU', 'MWF', 'GYPB', 'VK', 'JXQZ'],
     ['E', 'TAO', 'INSHR', 'DL', 'CU', 'MW', 'FGYPB', 'VK', 'JXQZ']]


def print_key(k: Dict[str, str]) -> None:
    _check_key(k)

    print(', '.join(map(lambda x: x + ' -> ' + k[x], k)))


def _iter_decrypt_key_permutations(k: Dict[str, str]) -> Dict[str, str]:
    k_e = _get_k_d(k)
    curr_k = dict(map(lambda x: (x, None), letter.LETTER_SET))

    total_num = 0
    for _letter_freq_groups in _letter_freq_groups_list:
        total_num += functools.reduce(operator.mul, map(lambda x: math.factorial(len(x)), _letter_freq_groups))
    print(total_num)

    curr_count = 0
    for _letter_freq_groups in _letter_freq_groups_list:
        for permutation in itertools.product(
                *map(lambda x: itertools.permutations(x) if x[0] != '#' else (x,), _letter_freq_groups)):

            # XXX: 用循环操作比用 map 操作，每百万操作快一两秒，怎么回事？
            # XXX: 用 zip 操作比用 map 操作还慢一两秒
            for i in range(len(permutation)):
                for j in range(len(permutation[i])):
                    curr_k[k_e[_letter_freq_groups[i][j]]] = \
                        permutation[i][j]
                # curr_k.update(map(lambda x, y: (k_e[x], y), \
                # _letter_freq_groups[i], permutation[i]))
                # curr_k.update(zip(map(lambda x: k_e[x], \
                # _letter_freq_groups[i]), permutation[i]))

            curr_count += 1
            if curr_count % 1048576 == 0:
                print("curr_count %d" % curr_count)

            yield curr_k

    return


# 返回格式为 [(-D, k_d), ...]
def get_most_likely_keys(c: str, n: int) -> List[key_d_entry]:
    freq = get_freq(c)
    k_d_base = get_base_decrypt_key(c)

    k_d_heap = []
    k_d_heap_throw_flag = False

    for k_d in _iter_decrypt_key_permutations(k_d_base):
        if not k_d_heap_throw_flag:
            heapq.heappush(k_d_heap, key_d_entry(-_get_distance(freq, k_d),
                                             k_d))
            if len(k_d_heap) == n:
                k_d_heap_throw_flag = True
        else:
            heapq.heappushpop(k_d_heap, key_d_entry(-_get_distance(freq, k_d), k_d))

    # 直接返回排序的即可，会按照 _k_d_entry 的第一项排序
    return sorted(k_d_heap)


def get_most_likely_plaintext(c: str, n: int, keys=None) -> List[str]:
    if keys is None:
        keys = get_most_likely_keys(c, n)

    # 应该把返回的 list 反转，因为 get_most_likely_keys 中 D 最小的元素在最后面
    return list(reversed(list(map(lambda x: decrypt(c, x[1]), keys))))


def main() -> None:
    _plaintext_filename = 'plaintext.txt'

    with open(_plaintext_filename, mode='r') as f:
        s = ''.join(f.readlines())

    s = ''.join(filter(lambda x: x.upper() in letter.LETTER_SET, s))
    print(s)

    k = dict(map(lambda x, y: (x, y), 'abcdefghijklmnopqrstuvwxyz'.upper(), 'qwertyuiopasdfghjklzxcvbnm'.upper()))

    c = encrypt(s, k)
    print(get_base_decrypt_key(c))
    keys = get_most_likely_keys(c, 10)
    print(keys)

    with open('tmp.txt', mode='w') as f:
        f.write(str(keys))

    print('\n'.join(get_most_likely_plaintext(c, 100, keys=keys)))


if __name__ == '__main__':
    main()
