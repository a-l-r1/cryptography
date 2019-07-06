from diffie_hellman import *

a_sk, a_pk = gen_key()
b_sk, b_pk = gen_key()

print(a_sk * b_pk == b_sk * a_pk)
