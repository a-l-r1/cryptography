# secrets 生成的是符合安全应用的随机数，但 Python 3.6 中才引入
import secrets

import gcd
import jacobi
import modular_exp


# 所有的概率素性测试算法返回 True 时只能保证为素数的概率至少为某个值，
# 但返回 False 时一定是合数
def miller_rabin(n: int, iterations: int) -> bool:
    if (n == 1):
        return False
        
    if (n == 2) or (n == 3):
        return True
    
    if (n % 2 == 0):
        return False
    
    q = n - 1
    k = 0
    
    while (q % 2 == 0):
        q //= 2
        k += 1

    for i in range(iterations):
        curr_pass_result = False
        
        # [0, n-3) = [0, n-4] -> [2, n-2]
        a = secrets.randbelow(n - 3)
        a += 2
        
        if (modular_exp.modular_exp(a, q, n) == 1):
            curr_pass_result = True
            continue
        
        for j in range(k):
            if (j == 0):
                curr_exponent = q
            else:
                curr_exponent *= 2
            
            if (modular_exp.modular_exp(a, curr_exponent, n) == n - 1):
                curr_pass_result = True
                break
        
        if (not curr_pass_result):
            return False
    
    return True

primality_test = miller_rabin

def fermat(n: int, iterations: int) -> bool:
    if (n == 1):
        return False
    
    if (n == 2) or (n == 3):
        return True
    
    if (n % 2 == 0):
        return False
    
    for i in range(iterations):
        # [0, n-1) = [0, n-2] -> [1, n-1]
        b = secrets.randbelow(n - 1)
        b += 1
        
        d = gcd.gcd(b, n)

        if (d > 1):
            return False
        
        if (modular_exp.modular_exp(b, n - 1, n) != 1):
            return False
    
    return True

def solovay_stassen(n: int, iterations: int) -> bool:
    if (n == 1):
        return False
    
    if (n == 2) or (n == 3) or (n == 5):
        return True
    
    if (n % 2 == 0):
        return False
    
    for i in range(iterations):
        # [0, n-5) -> [0, n-4] -> [2, n-2]
        b = secrets.randbelow(n - 5)
        b += 2
        
        r = modular_exp.modular_exp(b, (n - 1) // 2, n)
        
        # 如果 r 是 n - 1，把 r 设为 -1，以与 Jacobi 符号匹配
        if (r == n - 1):
            r = -1
        
        if (r != 1) and (r != -1):
            return False
        
        s = jacobi.jacobi(b, n)
        
        if (r != s):
            return False
    
    return True
