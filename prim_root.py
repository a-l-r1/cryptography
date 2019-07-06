import decimal, math

import exp, modular_exp, factor, phi, primality_test

_decimal_prec = 500
_decimal_eps = decimal.Decimal(10 ** -50)

# 返回能够满足 x ^ a == n 的最小整数 x （其中 a 是任意整数），以及最大的 a
# NOTE: 返回格式为 (x, a)
def _get_min_principle_nth_root(n: int) -> tuple:
    decimal.getcontext().prec = _decimal_prec
    
    n_decimal_ln = decimal.Decimal(n).ln()
    
    # 最坏的情况是 n 为 3 的某次幂
    max_exponent = n_decimal_ln / decimal.Decimal(3).ln()
    max_exponent = int(max_exponent + 1)
    
    # 从 max_exponent 到 2，倒着来是因为可以保证得到的结果一定是不能再开根号的
    for i in range(max_exponent, 1, -1):
        root = (n_decimal_ln / i).exp()
        
        if ((root - root.to_integral_value()).copy_abs() < \
            _decimal_eps):
            return (int(root.to_integral_value()), i)
    
    # 没有整数使它的某个次方等于 a
    return (n, 1)

_primality_test_iterations = 20

# NOTE：这里用到了 *概率性* 素性检验算法，因此合数被判断成素数的概率不为 0，但很小
# NOTE: 返回格式为 (is_power_of_prime, prime, exponent)
def _get_power_of_prime_stats(n: int) -> tuple:
    # 先看 n 本身是不是素数，因为有些应用场景里要求原根的数本来就是素数了
    if (primality_test.primality_test(n, _primality_test_iterations)):
        return (True, n, 1)
    
    x, a = _get_min_principle_nth_root(n)
    
    if (primality_test.primality_test(x, _primality_test_iterations)):
        return (True, x, a)
    
    return (False, None, None)

# NOTE: 返回格式为 (have_prim_root, is_half_power_of_prime, \
#    prime, exponent)
# NOTE: 若 n 为 2 * p ^ l 形式，prime ^ exponent == n // 2
def get_prim_root_stats(n: int) -> tuple:
    if (n == 2):
        return (True, False, 2, 1)
    
    if (n == 4):
        return (True, True, 2, 1)
    
    if (n % 4 == 0):
        return (False, False, None, None)
    
    if (n % 2 == 0):
        stats = _get_power_of_prime_stats(n // 2)
        
        return (stats[0], True and stats[0], stats[1], stats[2])
    else:
        stats = _get_power_of_prime_stats(n)

        return (stats[0], False, stats[1], stats[2])

def is_prim_root(x: int, modulus: int) -> bool:
    phi_modulus = phi.phi(modulus)
    phi_factor_dict = factor.factor(phi_modulus)
    
    for single_factor in phi_factor_dict.keys():
        if (modular_exp.modular_exp(x, phi_modulus // single_factor, \
            modulus) == 1):
            return False
    
    return True

# 获取最小的原根
def get_prim_root_generic(n: int) -> int:
    stats = get_prim_root_stats(n)
    p = stats[2]
    l = stats[3]
    
    if (stats[0] == False):
        raise ValueError("get_prim_root_generic: no primitive " + \
            "root of %d" % n)
    
    # 若 p == 2，则一定 n == 2 或 n == 4
    if (p == 2):
        # n == 4
        if stats[1]:
            return 3
        # n == 2
        else:
            return 1
    
    if stats[1]:
        modulus = n // 2
    else:
        modulus = n
    
    phi_modulus = phi.phi_prime_power(p, l)
    phi_factor_dict = factor.factor(p - 1)
    
    # 不存在的因数不应该加入字典
    if (l != 1):
        phi_factor_dict[p] = l - 1

    for i in range(2, n):
        failed_flag = False
        
        for single_factor in phi_factor_dict.keys():
            if (modular_exp.modular_exp(i, \
                phi_modulus // single_factor, modulus) == 1):
                failed_flag = True
                break

        if (failed_flag):
            continue
        else:
            return i
    
    # 不应该运行到这里
    raise RuntimeError("get_prim_root_generic: cannot find " + \
        "primitive root of %d while it must have one" % n)

get_prim_root = get_prim_root_generic

def get_prim_root_list(n: int) -> int:
    stats = get_prim_root_stats(n)
    p = stats[2]
    l = stats[3]
    
    if (stats[0] == False):
        raise ValueError("get_prim_root_generic: no primitive " + \
            "root of %d" % n)
    
    # 若 p == 2，则一定 n == 2 或 n == 4
    if (p == 2):
        # n == 4
        if stats[1]:
            return 3
        # n == 2
        else:
            return 1
    
    result = []
    
    modulus = exp.exp(p, l)
    
    phi_modulus = phi.phi_prime_power(p, l)
    phi_factor_dict = factor.factor(p - 1)
    
    # 不存在的因数不应该加入字典
    if (l != 1):
        phi_factor_dict[p] = l - 1

    for i in range(2, p):
        failed_flag = False
        
        for single_factor in phi_factor_dict.keys():
            if (modular_exp.modular_exp(i, \
                phi_modulus // single_factor, modulus) == 1):
                failed_flag = True
                break

        if (failed_flag):
            continue
        else:
            result.append(i)
    
    return result
