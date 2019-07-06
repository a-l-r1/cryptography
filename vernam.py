import itertools, operator

def _check_key(k: bytes) -> None:
    if len(k) == 0:
        raise ValueError("_check_key: empty key")

def encrypt(m: bytes, k: bytes) -> bytes:
    _check_key(k)
    # 使用 bytearray 预先分配空间，可以达到 O(n) 的时间复杂度
    # 否则 bytes 拼接的时间复杂度难以估计，且可能本身就是 O(n) 的
    result = bytearray(len(m))
    
    # 不会出现数组越界异常，因为 map 只能迭代出 len(m) 个对象
    index = 0
    for i in map(operator.xor, m, itertools.cycle(k)):
        result[index] = i
        index += 1

    return bytes(result)

def encrypt_nocheck(m: bytes, k: bytes) -> bytes:
    # 使用 bytearray 预先分配空间，可以达到 O(n) 的时间复杂度
    # 否则 bytes 拼接的时间复杂度难以估计，且可能本身就是 O(n) 的
    result = bytearray(len(m))
    
    # 不会出现数组越界异常，因为 map 只能迭代出 len(m) 个对象
    index = 0
    for i in map(operator.xor, m, itertools.cycle(k)):
        result[index] = i
        index += 1

    return bytes(result)

decrypt = encrypt
decrypt_nocheck = encrypt_nocheck
