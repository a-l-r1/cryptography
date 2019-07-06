import timeit

import bench, gcd

REPEAT_COUNT = 20

print(gcd.gcd_extended(7 ** 5, 5 ** 4))
print(gcd.gcd_generalized(7 ** 5, 5 ** 4))
print(gcd.gcd_iterative(7 ** 5, 5 ** 4))
print(gcd.get_modular_inverse(7 ** 5, 5 ** 4))

for x_digits in range(1000, 3000, 300):
    x = 10 ** x_digits
    modulus = 7 ** 100
    
    print("x 10^%d, modulus 7^100: " % x_digits)
    print('\n'.join(map(lambda x: "%s: time %f s, memory %f MB" % x, \
        bench.bench([gcd.gcd_generalized, gcd.gcd_extended], \
        [x, modulus], REPEAT_COUNT))))
