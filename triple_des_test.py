from triple_des import *


def main() -> None:
    k1 = bytes.fromhex('0123456789abcdef')
    k2 = bytes.fromhex('fedcba9876543210')
    k3 = bytes.fromhex('89abcdef01234567')
    p = bytes.fromhex('4242424242424242')

    c = encrypt(p, k1, k2, k3)
    print(c.hex())
    print(p == decrypt(c, k1, k2, k3))


if __name__ == '__main__':
    main()
