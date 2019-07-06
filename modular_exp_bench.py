import timeit

import bench, modular_exp

REPEAT_COUNT = 20

for power_digits in range(1, 7):
    x = 7 ** 400
    power = 10 ** power_digits
    modulus = 11 ** 300
    
    print("x 7^400, power 10^%d, modulus 11^300: " % \
        (power_digits))
    print('\n'.join(map(lambda x: "%s: time %f s, memory %f MB" % x, \
        bench.bench([modular_exp.square_modular_exp, \
            modular_exp.generic_modular_exp], \
        [x, power, modulus], REPEAT_COUNT))))

for power_digits in [7]:
    x = 7 ** 400
    power = 10 ** power_digits
    modulus = 11 ** 300
    
    print("x 7^400, power 10^%d, modulus 11^300: " % \
        (power_digits))
    print('\n'.join(map(lambda x: "%s: time %f s, memory %f MB" % x, \
        bench.bench([modular_pow.square_modular_pow], \
        [x, power, modulus], REPEAT_COUNT))))

for power_digits in range(100, 1000, 100):
    x = 7 ** 400
    power = 10 ** power_digits
    modulus = 11 ** 300
    
    print("x 7^400, power 10^%d, modulus 11^300: " % \
        (power_digits))
    print('\n'.join(map(lambda x: "%s: time %f s, memory %f MB" % x, \
        bench.bench([modular_exp.square_modular_exp], \
        [x, power, modulus], REPEAT_COUNT))))
