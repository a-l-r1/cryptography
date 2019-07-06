import functools, operator

import exp, factor

def phi(n: int) -> int:
    if (n == 1):
        return 1
    
    factor_dict = factor.factor(n)
    
    result = functools.reduce(operator.mul, map(lambda x: n - n // x , 
        factor_dict.keys()))
    result = result // exp.exp(n, len(factor_dict.keys()) - 1)
    
    return result

# 假定 p 是素数
def phi_prime_power(p: int, exponent: int) -> int:
    if (exponent < 0):
        raise ValueError("phi_prime_power: exponent < 0 unsupported")
    
    return (exp.exp(p, exponent - 1) * (p - 1))
