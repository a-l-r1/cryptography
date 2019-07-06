from elgamal_dss import *


def main() -> None:
    m = b'hello, world'
    sk, pk = gen_key()
    print(sk, pk)

    sig = sign(m, sk)
    print(sig)

    m1 = b'hello, world1'
    print(verify(m, pk, sig))
    print(verify(m1, pk, sig))


if __name__ == '__main__':
    main()
