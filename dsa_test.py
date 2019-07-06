from dsa import *


sk, pk = gen_key()
print(sk, pk)

m = b'hello world'
sig = sign(m, sk)
print(sig)

result = verify(m, pk, sig)
print(result)

m1 = b'hello world1'
result1 = verify(m1, pk, sig)
print(result1)
