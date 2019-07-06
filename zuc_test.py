from zuc import *


def main() -> None:
    k = bytes(128 // 8)
    iv = bytes(128 // 8)

    result = bytes(gen_key_iter(k, iv, 8))
    print(result.hex())
    print(result == bytes.fromhex('27bede74018082da'))

    k = bytes.fromhex('ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff')
    iv = bytes.fromhex('ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff')

    result = bytes(gen_key_iter(k, iv, 8))
    print(result.hex())
    print(result == bytes.fromhex('0657cfa07096398b'))

    k = bytes.fromhex('3d 4c 4b e9 6a 82 fd ae b5 8f 64 1d b1 7b 45 5b')
    iv = bytes.fromhex('84 31 9a a8 de 69 15 ca 1f 6b da 6b fb d8 c7 66')

    result = bytes(gen_key_iter(k, iv, 8))
    print(result.hex())
    print(result == bytes.fromhex('14f1c2723279c419'))

    m = b'hello world'
    c = encrypt(k, iv, m)
    m_recovered = decrypt(k, iv, c)
    print(c.hex())
    print(m == m_recovered)


if __name__ == '__main__':
    main()