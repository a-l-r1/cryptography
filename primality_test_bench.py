import secrets

import bench, primality_test, prime_sieve

REPEAT_COUNT = 20

ITERATIONS = 20

print("checking random numbers")
for bit_length in range(100, 500+100, 100):
    print("bit length %d: " % bit_length)
    
    bench.bench_output([primality_test.fermat, \
        primality_test.miller_rabin, primality_test.solovay_stassen], \
        [secrets.randbits(bit_length), ITERATIONS], REPEAT_COUNT)

print("checking 43 the prime")
for iterations in range(10, 100+10, 10):
    print("iterations %d: " % iterations)
    
    bench.bench_output([primality_test.fermat, \
        primality_test.miller_rabin, primality_test.solovay_stassen], \
        [43	, ITERATIONS], REPEAT_COUNT)
