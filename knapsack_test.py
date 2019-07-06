from knapsack import *
from bit_string import BitString

key_length = 5
key = gen_key(key_length)
print(key)
sk, pk = key

m = BitString('10101')
c = encrypt(m, pk)
print(c)
m_recovered = decrypt(c, sk)
print(m_recovered)
print(m_recovered == m)

w = [2, 3, 7, 14, 30, 57, 120, 251]
q = 491
r = 41
sk = (w, q, r)

pk = [82, 123, 287, 83, 248, 373, 10, 471]

m = BitString('00101111')
c = encrypt(m, pk)
print(c)

m_recovered = cryptanalysis_lll(c, pk)
print(m_recovered)
print(m == m_recovered)
