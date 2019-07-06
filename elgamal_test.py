from elgamal import *

sk, pk = gen_key()

encrypt_file('plaintext.txt', 'ciphertext.txt', pk)
decrypt_file('plaintext_recovered.txt', 'ciphertext.txt', sk)
