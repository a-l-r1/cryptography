import gcd

import secrets

# 以下的操作都是采用列表表示，元素是 (deg, coeff)，列表中的多项式系数从小到大排列
# 为了效率，各方法的参数都是整数，但其实应该给多项式新建一个类
def _check_deg(deg: int) -> None:
    if (deg < 0):
        raise ValueError("check_deg: deg < 0")

def _check_deg_positive(deg: int) -> None:
    if (deg <= 0):
        raise ValueError("check_deg_positive: deg <= 0")

def z_x_gen_prim_poly_simple_nocheck(deg: int) -> list:
    # x ^ n + 2
    return [(0, 2), (deg, 1)]

def z_x_gen_prim_poly_simple(deg: int) -> list:
    _check_deg_positive(deg)
    
    return z_x_gen_prim_poly_simple_nocheck(deg)

def z_x_gen_prim_poly_random_nocheck(deg: int, max_coeff: int) -> list:
    result = [(i, secrets.randbelow(max_coeff + 1)) for i in range(deg)]
    result += [(deg, 1)]
    
    result = list(filter(lambda x: x[1] != 0, result))

    return result

def z_x_gen_prim_poly_random(deg: int, max_coeff: int) -> list:
    _check_deg_positive(deg)
    
    return z_x_gen_prim_poly_random_nocheck(deg, max_coeff)
