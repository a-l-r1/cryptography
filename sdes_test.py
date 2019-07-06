from sdes import *


def main() -> None:
    k1 = BitString('0100010000')
    k2 = BitString('1010111001')
    p1 = BitString('10010011')
    p2 = BitString('00000000')
    p3 = BitString('10011101')
    c1 = double_sdes_encrypt(p1, k1, k2)
    c2 = double_sdes_encrypt(p2, k1, k2)
    c3 = double_sdes_encrypt(p3, k1, k2)

    result = double_sdes_cryptanalysis_mitm([p1, p2, p3], [c1, c2, c3])
    print('\n'.join(map(str, result)))
    print(len(result))

    print((k1, k2) in result)

    for key_pair in result:
        if list(map(lambda x: double_sdes_encrypt(x, k1, k2), [p1, p2, p3])) != [c1, c2, c3]:
            print(key_pair)


if __name__ == '__main__':
    main()
