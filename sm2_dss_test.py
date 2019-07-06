from sm2_dss import *


def main() -> None:
    id_ = b'ALICE123@YAHOO.COM'
    print(id_.hex())

    d_a = 0x128B2FA8_BD433C6C_068C8D80_3DFF7979_2A519A55_171B1B65_0C23661D_15897263

    x_a = 0x0AE4C779_8AA0F119_471BEE11_825BE462_02BB79E2_A5844495_E97C04FF_4DF2548A
    y_a = 0x7C0240F8_8F1CD4E1_6352A73C_17B7F16F_07353E53_A176D684_A9FE0C6B_B798E857
    p_a = ECPoint(ec, fp(x_a), fp(y_a))
    print(p_a)

    z_a = get_user_hash(id_, p_a)
    print(z_a.hex())
    print(z_a == bytes.fromhex("F4A38489 E32B45B6 F876E3AC 2168CA39 "
                               "2362DC8F 23459C1D 1146FC3D BFB7BC9A "))

    m = b'message digest'
    sig = sign(m, d_a, z_a)
    # print(sig == bytes.fromhex("40F1EC59 F793D9F4 9E09DCEF 49130D41 "
    #                            "94F79FB1 EED2CAA5 5BACDB49 C4E755D1 "
    #                            "6FC6DAC3 2C5D5CF1 0C77DFB2 0F7C2EB6 "
    #                            "67A45787 2FB09EC5 6327A67E C7DEEBE7 "))

    result = verify(m, p_a, sig, z_a)
    print(result)

    m1 = b'message digest1'
    result1 = verify(m1, p_a, sig, z_a)
    print(result1)

    z_a1 = z_a + bytes((0x01,))
    result2 = verify(m, p_a, sig, z_a1)
    print(result2)

    sk, pk = gen_key()
    sig = sign(m, sk, z_a)
    result3 = verify(m, pk, sig, z_a)
    print(result3)


if __name__ == '__main__':
    main()
