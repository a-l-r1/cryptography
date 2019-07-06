from ec import EC, ECPoint
import finite_field

'''
p = 0xFFFFFFFE_FFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF_00000000_FFFFFFFF_FFFFFFFF
a = 0xFFFFFFFE_FFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF_00000000_FFFFFFFF_FFFFFFFC
b = 0x28E9FA9E_9D9F5E34_4D5A9E4B_CF6509A7_F39789F5_15AB8F92_DDBCBD41_4D940E93
n = 0xFFFFFFFE_FFFFFFFF_FFFFFFFF_FFFFFFFF_7203DF6B_21C6052B_53BBF409_39D54123
Gx = 0x32C4AE2C_1F198119_5F990446_6A39C994_8FE30BBF_F2660BE1_715A4589_334C74C7
Gy = 0xBC3736A2_F4F6779C_59BDCEE3_6B692153_D0A9877C_C62A4740_02DF32E5_2139F0A0

fp = finite_field.get_prime_finite_field_element_class(p, '_fp')
ec = EC(fp(a), fp(b))
g = ECPoint(ec, fp(Gx), fp(Gy))
'''

p = 0x8542D69E_4C044F18_E8B92435_BF6FF7DE_45728391_5C45517D_722EDB8B_08F1DFC3
a = 0x787968B4_FA32C3FD_2417842E_73BBFEFF_2F3C848B_6831D7E0_EC65228B_3937E498
b = 0x63E4C6D3_B23B0C84_9CF84241_484BFE48_F61D59A5_B16BA06E_6E12D1DA_27C5249A
n = 0x8542D69E_4C044F18_E8B92435_BF6FF7DD_29772063_0485628D_5AE74EE7_C32E79B7
Gx = 0x421DEBD6_1B62EAB6_746434EB_C3CC315E_32220B3B_ADD50BDC_4C4E6C14_7FEDD43D
Gy = 0x0680512B_CBB42C07_D47349D2_153B70C4_E5D7FDFC_BFA36EA1_A85841B9_E46E09A2

fp = finite_field.get_prime_finite_field_element_class(p, '_fp')
ec = EC(fp(a), fp(b))
g = ECPoint(ec, fp(Gx), fp(Gy))