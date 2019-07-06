import datetime

import bench
import aes
import aes_optimized

REPEAT_COUNT = 20

p = bytes.fromhex('54776F204F6E65204E696E652054776F')
k = bytes.fromhex('5468617473206D79204B756E67204675')

bench.bench_output([aes.encrypt, aes_optimized.encrypt], [p, k], REPEAT_COUNT)

t1 = datetime.datetime.now()
aes.encrypt_file('plaintext.txt', 'ciphertext.txt', k)
t2 = datetime.datetime.now()

aes.decrypt_file('plaintext_recovered.txt', 'ciphertext.txt', k)

print(t2 - t1)
