import math

# 生成初始的质数分布表，表中索引为 i 的项表示 i 是否为质数，因此长度为上界 + 1
# 由于是初始的质数分布表，假定所有数都是质数
def gen_dist_table(upper_bound:int) -> list:
    return [True for i in range(upper_bound+1)]

def _eratosthenes(dist_table:list) -> list:
    upper_bound = len(dist_table)-1
    prime_list = []

    ceil_sqrt_upper_bound = math.ceil(math.sqrt(upper_bound))

    # 0 和 1 都不是质数
    dist_table[0] = dist_table[1] = False

    for i in range(2, ceil_sqrt_upper_bound+1):
        if (not dist_table[i]):
            continue
        else:
            prime_list.append(i)

        for j in range(i*i, upper_bound+1, i):
            dist_table[j] = False

    for i in range(ceil_sqrt_upper_bound+1, upper_bound+1):
        if (dist_table[i]):
            prime_list.append(i)

    return prime_list

def eratosthenes(upper_bound:int) -> list:
	return _eratosthenes(gen_dist_table(upper_bound))

def _eratosthenes_precompute(dist_table:list) -> list:
    upper_bound = len(dist_table)-1
    initial_prime_list = []
    prime_list = []
    
    ceil_sqrt_upper_bound = math.ceil(math.sqrt(upper_bound))
    
    # 0 和 1 都不是质数
    dist_table[0] = dist_table[1] = False

    for i in range(2, ceil_sqrt_upper_bound+1):
        if (not dist_table[i]):
            continue
        else:
            for j in range(2*i, ceil_sqrt_upper_bound+1, i):
                dist_table[j] = False
            
            initial_prime_list.append(i)
            prime_list.append(i)
    
    for i in range(ceil_sqrt_upper_bound+1, upper_bound+1):
        for j in initial_prime_list:
            if (i % j == 0):
                dist_table[i] = False
                break
        
        if (dist_table[i]):
            prime_list.append(i)
    
    return prime_list

def eratosthenes_precompute(upper_bound:int) -> list:
    return _eratosthenes_precompute(gen_dist_table(upper_bound))

def _euler(dist_table:list) -> list:
    upper_bound = len(dist_table)-1
    prime_list = []

    dist_table[0] = dist_table[1] = False

    for i in range(2, upper_bound):
        if (dist_table[i]):
            prime_list.append(i)

        # 遍历已经找到的每个素数，将当前数与相应素数的积标记为合数
        for j in prime_list:
            # 保证不超出边界
            if (i * j > upper_bound):
                break

            dist_table[i*j] = False

            # 之后没有必要再筛，因为之后 i 与比 j 更大的素数的乘积
            # 可以分解成 j 与一个比 i 更大的数的乘积
            # 这样保证了 j 为 i 的最小质因子和算法的线性性
            if (i % j == 0):
                break

    return prime_list

def euler(upper_bound:int) -> list:
	return _euler(gen_dist_table(upper_bound))
