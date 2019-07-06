from random import randrange

def jacobi(a: int, n: int) -> int:
    if (n % 2 == 0):
        ValueError("jacobi: (%d, %d): n must be positive and odd" % \
            (a, n))
    
    a = a % n
    
    if (a < 0):
        a = a + n
    
    t = 1
    while (a != 0):
        while (a % 2 == 0):
            a //= 2
            if (n % 8 == 3) or (n % 8 == 5):
                t = -t
        
        a, n = n, a
        
        if (a % 4 == n % 4) and (n % 4 == 3):
            t = -t
        
        a = a % n
    
    if n == 1:
        return t
    else:
        return 0
