from des import *

print(str(encrypt(bytes.fromhex('0123456789abcdef'), bytes.fromhex('133457799bbcdff1')).hex())
      == '85e813540f0ab405')
print(decrypt(bytes.fromhex('85e813540f0ab405'), bytes.fromhex('133457799bbcdff1')).hex())
print(str(encrypt(bytes.fromhex('8787878787878787'), bytes.fromhex('0e329232ea6d0d73')).hex())
      == '0000000000000000')
print(decrypt(bytes.fromhex('0000000000000000'), bytes.fromhex('0e329232ea6d0d73')).hex())

print(des_3round_encrypt(bytes.fromhex('0123456789abcdef'), bytes.fromhex('133457799bbcdff1')).hex())
print(des_3round_encrypt(bytes.fromhex('1111111189abcdef'), bytes.fromhex('133457799bbcdff1')).hex())
print(des_3round_encrypt(bytes.fromhex('29182300acacacac'), bytes.fromhex('133457799bbcdff1')).hex())
print(des_3round_encrypt(bytes.fromhex('129308afacacacac'), bytes.fromhex('133457799bbcdff1')).hex())
print(des_3round_encrypt(bytes.fromhex('748502CD38451097'), bytes.fromhex('1a624c89520dec46')).hex())

p_list = [
    '748502CD38451097', '3874756438451097',
    '357418DA013FEC86', '12549847013FEC86',
    '486911026ACDFF31', '375BD31F6ACDFF31'
]
p_list = list(map(bytes.fromhex, p_list))

c_list = [
    '03C70306D8A09F10', '78560A0960E6D4CB',
    'D8A31B2F28BBC5CF', '0F317AC2B23CB944',
    '45FA285BE5ADC730', '134F7915AC253457'
]
c_list = list(map(bytes.fromhex, c_list))

print('\n'.join(map(bytes.hex, des_3round_cryptanalysis_differential(p_list, c_list))))


def file_op_demo() -> None:
    k = bytes.fromhex(input('enter hex of key: '))

    p_name = input('enter filename of plaintext: ')
    c_name = input('enter filename of ciphertext: ')
    p_recovered_name = input('enter filename of recovered plaintext: ')

    encrypt_file(p_name, c_name, k)
    decrypt_file(p_recovered_name, c_name, k)


file_op_demo()
