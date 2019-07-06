import timeit

import bench, prime_sieve

REPEAT_COUNT = 1

for upper_bound_digits in range(7, 9):
    upper_bound = 10 ** upper_bound_digits
    
    print("upper_bound %d: " % upper_bound )
    print('\n'.join(map(lambda x: "%s: time %f s, memory %f MB" % x, \
        bench.bench([prime_sieve.eratosthenes, prime_sieve.euler], \
        [upper_bound], REPEAT_COUNT))))
