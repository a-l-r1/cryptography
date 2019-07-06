# 这里也应该用 secrets 模块，为了避免敌手推断出随机数生成器状态
import decimal, math, secrets

import gcd

_decimal_prec = 500
_decimal_eps = decimal.Decimal(10 ** -50)

# 返回格式为 {factor: degree}
def generic(n: int) -> dict:
    decimal.getcontext().prec = _decimal_prec
    # 该函数只用向上取整模式
    decimal.getcontext().rounding = decimal.ROUND_CEILING
    
    result = {}
    
    if (n == 1) or (n == 2) or (n == 3):
        result[n] = 1
        return result
    
    if (n % 2 == 0):
        result[2] = 0
        
        while (n % 2 == 0):
            n //= 2
            result[2] += 1
    
    curr_factor = 3
    
    ceil_sqrt_n = decimal.Decimal(n).sqrt().to_integral_value()
    
    while (n != 1):
        if (n % curr_factor == 0):
            result[curr_factor] = 0
            
            while (n % curr_factor == 0):
                n //= curr_factor
                result[curr_factor] += 1
                
            # 只有 n 被某个质数全除完时，才更新 n
            ceil_sqrt_n = decimal.Decimal(n).sqrt().to_integral_value()
    
        curr_factor += 2
        
        # 当前因数超过了 sqrt(n)，没必要分解了
        if (curr_factor > ceil_sqrt_n):
            # 注意这时 n 可能被分解完
            if (n != 1):
                result[n] = 1
            return result
    
    return result

factor = generic

"""
def pollard_rho(n: int) -> dict:
    result = {}
    
    if (n == 1) or (n == 2) or (n == 3):
        result[n] = 1
        return result
    
    if (n % 2 == 0):
        result[2] = 0
        
        while (n % 2 == 0):
            n //= 2
            result[2] += 1
    
    while (n != 1):
        factor = 1
        cycle_size = 2
        
        x = 2
        x_fixed = 2
        
        while (factor == 1):
            count = 1
            
            while (count <= cycle_size) and (factor == 1):
                x = (x * x + 1) % n
                factor = gcd.gcd(x - x_fixed, n)
                count += 1
            
            cycle_size *= 2
            x_fixed = x
        
        n //= factor
"""
