# 把 a 和 b 都取绝对值，并且保证 a >= b
def gcd_normalize(a: int, b: int) -> tuple:
    result = tuple(map(abs, (a, b)))

    if (result[0] < result[1]):
        result = (result[1], result[0])

    return result


def _gcd_iterative(a: int, b: int) -> int:
    while (b != 0):
        a = a % b
        a, b = b, a

    return a


def gcd_iterative(a: int, b: int) -> int:
    a, b = gcd_normalize(a, b)

    return _gcd_iterative(a, b)


gcd = gcd_iterative


def _gcd_recursive(a: int, b: int) -> int:
    if (b == 0):
        return a

    return _gcd_recursive(b, a % b)


def gcd_recursive(a: int, b: int) -> int:
    a, b = gcd_normalize(a, b)

    return _gcd_recursive(a, b)


def is_coprime(a: int, b: int) -> bool:
    return gcd(a, b) == 1


def gcd_extended(a: int, b: int) -> list:
    # NOTE: 以下的 tuple 都以 (q, r, s, t) 格式保存数据
    # NOTE: 不要正规化，调用者期望保持 a 和 b 的次序和符号
    # NOTE: 返回每一步计算结果的列表

    last_last_result = (0, a, 1, 0)
    last_result = (0, b, 0, 1)
    result = (None, None, None, None)

    # 保存前两次规定下的结果
    log_list = [last_last_result, last_result]

    while True:
        quotient = last_last_result[1] // last_result[1]
        remainder = last_last_result[1] % last_result[1]

        result = (quotient, remainder, \
                  last_last_result[2] - quotient * last_result[2], \
                  last_last_result[3] - quotient * last_result[3])

        log_list.append(result)

        if (remainder == 0):
            break

        # 循环移动结果
        last_last_result, last_result, result = \
            last_result, result, (None, None, None, None)

    return log_list


def _gcd_generalized_get_coeff(initial: tuple, q: list) -> int:
    # NOTE: initial 形如 (x[-2], x[-1])
    last_last_result = initial[0]
    last_result = initial[1]
    result = None

    for q_ in q:
        result = last_last_result - q_ * last_result

        last_last_result, last_result, result = \
            last_result, result, None

    return last_last_result


def gcd_generalized(a: int, b: int) -> tuple:
    # NOTE: 不要正规化，调用者期望保持 a 和 b 的次序和符号
    # NOTE: 返回 (gcd, s, t)

    q = [0, 0]
    r = [a, b]

    while (r[-1] != 0):
        q.append(r[-2] // r[-1])
        r.append(r[-2] % r[-1])

    gcd = r[-2]
    s = _gcd_generalized_get_coeff((1, 0), q)
    t = _gcd_generalized_get_coeff((0, 1), q)

    return (gcd, s, t)


def get_modular_inverse(x: int, modulus: int) -> int:
    gcd, s, t = gcd_generalized(x, modulus)

    if (gcd != 1):
        raise ValueError("get_modular_inverse: not coprime: %d %% %d" \
                         % (x, modulus))

    # 如果模数为 1，gcd == 1，但是 s == 0，这是一种特殊情况
    if s == 0:
        raise ValueError("get_modular_inverse: s == 0: %d %% %d" \
                         % (x, modulus))

    return s % modulus


def get_gcd_inverse(x: int, modulus: int) -> int:
    gcd, s, t = gcd_generalized(x, modulus)

    # 如果模数为 1，gcd == 1，但是 s == 0，这是一种特殊情况
    if (s == 0):
        raise ValueError("get_modular_inverse: s == 0: %d %% %d" \
                         % (x, modulus))

    return (s % modulus)
