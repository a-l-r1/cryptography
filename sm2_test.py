from sm2 import *


def main() -> None:
    m = b'encryption standard'
    print(m.hex())

    d_b = 0x1649AB77_A00637BD_5E2EFE28_3FBF3535_34AA7F7C_B89463F2_08DDBC29_20BB0DA0
    d_b = fp(d_b)

    x_b = 0x435B39CC_A8F3B508_C1488AFC_67BE491A_0F7BA07E_581A0E48_49A5CF70_628A7E0A
    y_b = 0x75DDBA78_F15FEECB_4C7895E2_C1CDF5FE_01DEBB2C_DBADF453_99CCF77B_BA076A42
    p_b = ECPoint(ec, fp(x_b), fp(y_b))

    c = encrypt(m, p_b)
    print(c.hex())

    """
    print(c == bytes.fromhex(
        "04245C26 FB68B1DD DDB12C4B 6BF9F2B6 D5FE60A3 83B0D18D 1C4144AB F17F6252 "
        "E776CB92 64C2A7E8 8E52B199 03FDC473 78F605E3 6811F5C0 7423A24B 84400F01 "
        "B8650053 A89B41C4 18B0C3AA D00D886C 00286467 9C3D7360 C30156FA B7C80A02 "
        "76712DA9 D8094A63 4B766D3A 285E0748 0653426D"))
    """

    m_ = decrypt(c, d_b)
    print(m_.hex())
    print(m == m_)

    encrypt_file('plaintext.txt', 'ciphertext.txt', p_b)
    decrypt_file('plaintext_recovered.txt', 'ciphertext.txt', d_b)

    with open('plaintext.txt', 'rb') as pt_f, open('plaintext_recovered.txt', 'rb') as pt_r_f:
        print(pt_f.read() == pt_r_f.read())


if __name__ == '__main__':
    main()
